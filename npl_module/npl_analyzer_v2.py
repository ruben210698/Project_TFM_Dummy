"""
Con spicy NPL quiero pasarle una frase y que me saque las caracteristicas morg¡fologicas y sintacticas de cada palabra.
Tambien quiero que cree relaciones entre ellas.
"""
import re
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy.tokens import Doc
from spacy.tokens import Token
from spacy.symbols import nsubj, VERB
from spacy.lang.es import Spanish
from spacy.lang.es.stop_words import STOP_WORDS
from spacy.lang.es.examples import sentences
from spacy.pipeline import EntityRuler
from spacy.pipeline import EntityRecognizer
from spacy.pipeline import EntityLinker
from spacy.pipeline import EntityRuler

from npl_module import token_manual_modifier
from utils.Palabra import Palabra
from utils.Relacion import Relacion
from constants.type_morfologico import *
from constants.type_sintax import *
from utils.TokenNLP import TokenNLP, TYPE_RELACION, TYPE_PALABRA
from utils.utils_text import son_pal_rel_contiguas
# from visualizacion.graficoFinal2 import print_graph
from visualizacion.grafico14 import print_graph, generate_graph

nlp = spacy.load("es_core_news_lg")

#LIST_TYPES_CONNECTOR_RELATION = [TYPE_MORF_ADP, TYPE_MORF_ADP, TYPE_MORF_CONJ, TYPE_MORF_CCONJ, TYPE_MORF_SCONJ,
#                                 TYPE_MORF_DET, TYPE_MORF_PRON, TYPE_MORF_PART, TYPE_MORF_VERB, TYPE_MORF_AUX]



#LIST_TYPES_SINTAX_RELATION = [TYPE_SINTAX_ADVMOD, TYPE_SINTAX_NPADVMOD]





def get_list_palabras_relaciones(texto,spacy_load):
    list_token_nlp_oraciones = preprocesing_oracion_nlp(texto, spacy_load)

    list_palabras = get_list_palabras(list_token_nlp_oraciones)
    list_relaciones = get_list_relaciones(list_palabras)

    # Sacar las palabras que no se han sacado antes, omitiendo las Ys (que ya se verá como hacer enumeraciones después)
    # Y hay que comprobar que, si una palabra es igual a la que hay en la relación, no se ponga (en minusculas y sin acentos)
    for oracion in list_token_nlp_oraciones:
        for token in oracion:
            if token.representado:
                continue
            else:
                if token.tipo_morfol == TYPE_MORF_CCONJ:
                    continue
                if token.token_nlp_padre is not None:
                    pal_padre = token.token_nlp_padre.palabra_que_representa
                    rel_dest_padre = Palabra.relaciones_dict_destino.get(pal_padre)
                    entontrada = False
                    if rel_dest_padre is not None and rel_dest_padre != []:
                        for rel in rel_dest_padre:
                            if rel.texto == token.text or rel.texto.__contains__(' ' + token.text + ' '):
                                entontrada = True
                                break
                    if entontrada:
                        continue
                    # Si no esta en la relacion, se lo añado a la palabra, ya que no tiene relación hijo
                    pal_padre.add_aux_text(token.text, token.position_doc)


                print("hola")
                print(token)

    return list_palabras, list_relaciones


def get_list_relaciones(list_palabras):
    list_relaciones = []
    for palabra in list_palabras:
        token_nlp = palabra.token_nlp
        if token_nlp.palabra_padre_final is None:
            continue

        list_rel_padre = token_nlp.tokens_relacion_padre_final

        if list_rel_padre != []:
            for token_rel in list_rel_padre:
                pal_origen = token_nlp.palabra_padre_final
                pal_dest = palabra
                if pal_dest.lugar_sintactico == TYPE_SINTAX_NSUBJ:
                    pal_origen = palabra
                    pal_dest = token_nlp.palabra_padre_final
                nueva_relacion = Relacion(
                    texto=token_rel.text,
                    pal_origen=pal_origen,
                    pal_dest=pal_dest,
                    position_doc=token_rel.position_doc,
                    lugar_sintactico=token_nlp.tipo_sintagma)
                list_relaciones.append(nueva_relacion)
                token_rel.representado = True
                token_rel.list_rel_que_representa.append(nueva_relacion)
            print(list_rel_padre)
        else:
            # Relación sin texto
            pal_origen = token_nlp.palabra_padre_final
            pal_dest = palabra
            if pal_dest.lugar_sintactico == TYPE_SINTAX_NSUBJ:
                pal_origen = palabra
                pal_dest = token_nlp.palabra_padre_final
            nueva_relacion = Relacion(
                texto='',
                pal_origen=pal_origen,
                pal_dest=pal_dest,
                position_doc=token_nlp.position_doc,
                lugar_sintactico=token_nlp.tipo_sintagma)
            list_relaciones.append(nueva_relacion)
    return list_relaciones


def get_list_palabras(list_token_nlp_oraciones):
    list_palabras = []
    for oracion_nlp in list_token_nlp_oraciones:
        for token_nlp in oracion_nlp:
            if token_nlp.tipo_palabra is TYPE_PALABRA:
                if (token_nlp.tipo_morfol == 'AUX' and token_nlp.token_nlp_padre.tipo_morfol == 'VERB') or \
                        (token_nlp.tipo_morfol == 'PRON' and token_nlp.token_nlp_padre.tipo_morfol == 'VERB'):
                    # Es el auxiliar de un verbo (ha saltado, se ha comido...)
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    nueva_palabra.add_aux_text(token_nlp.text, token_nlp.position_doc)
                else:
                    nueva_palabra = Palabra.constructor_alternativo(token_nlp=token_nlp)
                    list_palabras.append(nueva_palabra)

                token_nlp.representado = True
                token_nlp.palabra_que_representa = nueva_palabra
                for child in token_nlp.list_children_nlp:
                    child.palabra_padre_final = nueva_palabra

            if token_nlp.tipo_palabra is TYPE_RELACION:
                # De momento no creo la relacion, solo guardo el token en tokens_relacion_padre_final
                for child in token_nlp.list_children_nlp:
                    child.palabra_padre_final = token_nlp.palabra_padre_final  # Si es relacion, hereda el padre del padre
                    child.tokens_relacion_padre_final.append(token_nlp)
        print(oracion_nlp)
    return list_palabras


def analyse_token_recursive(token_padre, token_actual, num_oracion):
    new_list_token_nlp = []
    if TokenNLP.nlp_token_dict.get(token_actual.idx, None) is not None or \
            (token_actual.pos_ == TYPE_MORF_PUNCT and token_actual.lemma_ == '.'):
        return []

    new_token_nlp = TokenNLP(token_actual, num_oracion, token_padre, token_actual.children)
    new_list_token_nlp.append(new_token_nlp)

    print(token_actual)
    for child in token_actual.children:
        new_list_token_nlp_2 = analyse_token_recursive(token_actual, child, num_oracion)
        new_list_token_nlp = new_list_token_nlp + new_list_token_nlp_2

    return new_list_token_nlp



def preprocesing_oracion_nlp(texto, spacy_load):
    texto = texto.replace('\n', '. ').replace('\r', '. ').replace('\t', '. ').\
        replace("    ", " ").replace("   ", " ").replace("  ", " ")

    nlp = spacy.load(spacy_load)
    doc = nlp(texto)

    ## Primero lo divido en oraciones
    list_token_oraciones = []
    list_token_nlp_oraciones = []
    list_oracion_actual = []

    get_list_token_oraciones(doc, list_oracion_actual, list_token_oraciones)

    # Después, recorro la oración empezando por el Root
    num_oracion = -1
    for list_token_oracion in list_token_oraciones:
        num_oracion += 1
        list_token_nlp = []

        print("Oracion: ", num_oracion)
        # Ordenar la lista de tokens de la oracion por el número de children
        list_token_oracion.sort(key=lambda x: len(list(x.children)), reverse=True)
        # sacar de list_token_oracion el elemento cuyo token.dep_ == ROOT
        root = None
        for token in list_token_oracion:
            if token.dep_ == TYPE_SINTAX_ROOT:
                root = token
                break
        if root is not None:
            list_token_oracion.remove(root)
            list_token_oracion.insert(0, root)
        # Recorrer tokens y buscar palabras y relaciones
        for token in list_token_oracion:
            list_texts_ok = [token.text for token in list_token_nlp]
            if token.text not in list_texts_ok or not (token.pos_ == TYPE_MORF_PUNCT and token.lemma_ == '.'):
                list_token_nlp_2 = analyse_token_recursive(None, token, num_oracion)
                list_token_nlp = list_token_nlp + list_token_nlp_2

        for token_nlp in list_token_nlp:
            token_nlp.refresh_parents_children()
        # quitar todos los tokens que sean de tipo puntuacion
        list_token_nlp = [token_nlp for token_nlp in list_token_nlp if token_nlp.tipo_morfol != TYPE_MORF_PUNCT]
        list_token_nlp_oraciones.append(list_token_nlp)

    return list_token_nlp_oraciones


def get_list_token_oraciones(doc, list_oracion_actual, list_token_oraciones):
    for token in doc:
        ########################################
        print(token.text, ": ", token.idx, token.lemma_, "|| pos_:", token.pos_, "|| tag_:", token.tag_,
              "|| dep_:", token.dep_, token.shape_, token.is_alpha, token.is_stop)
        for child in token.children:
            print("-->child:", child)
        ########################################
        tipo_morfol = token.pos_

        if tipo_morfol == TYPE_MORF_PUNCT and token.lemma_ == ".":
            # TODO hacer y que solo lo haga con los puntos, no con las comas.
            list_token_oraciones.append(list_oracion_actual)
            list_oracion_actual = []
            continue
        else:
            list_oracion_actual.append(token)
    if list_oracion_actual not in list_token_oraciones:
        list_token_oraciones.append(list_oracion_actual)


texto = "Mi perro y mi gato juegan juntos en el parque con una pelota"

#texto = "Mi perro, mi gato y mi loro juegan juntos en el parque con una pelota"


texto = "Mi perro es un golden retriever de tres años que adora jugar con su pelota en el parque y siempre me da la bienvenida moviendo la cola cuando llego a casa."
texto = "El sol brilla en el cielo azul los pájaros cantan en los árboles verdes el viento sopla suavemente a través de las hojas en el campo las vacas pastan tranquilamente en la ciudad la gente camina apresurada por las calles en el mar los barcos navegan en aguas cristalinas en todas partes la naturaleza sigue su curso y el mundo sigue girando."
texto = "La vida es como un viaje en el que cada uno elige su propio camino a veces es fácil otras veces es difícil hay momentos de alegría y momentos de tristeza pero sin importar qué tan difícil sea el camino siempre hay algo que aprender cada experiencia buena o mala nos ayuda a crecer y a ser más fuertes la naturaleza nos rodea y nos regala su belleza y su sabiduría hay que aprender a apreciarla y cuidarla al final del camino lo importante no es lo que hayamos acumulado sino las personas que hayamos tocado y las huellas que hayamos dejado en el mundo."
texto = "Mi novia tiene una toalla de hospital para su perro"


#texto = "Isthar come paja en el pajar mientras Jasper le mira mientras Tina caza palomas para cenar"
#texto = "Mi perro y mi gato juegan juntos en el parque con una pelota"
#texto = "Me llamo Rubén y tengo 25 años. Vivo en Madrid y trabajo en una empresa de tecnología. Me gusta leer, viajar y pasar tiempo con mi familia y amigos."
#texto = "Los Austrias gobernaron España en el siglo XVI y XVII, responsables también de la Inquisición, expulsión de judíos. Su legado: arquitectura y arte en Madrid y Córdoba."
#texto = "Ruben cocina hamburguesas en la Freidora de aire"
#texto = "La naturaleza es impresionante en su variedad de paisajes, desde montañas majestuosas y extensas llanuras hasta océanos y ríos caudalosos."

#TEST Flat
texto = "Felipe II fué rey de españa hace tiempo. Maria Antonieta era reina de Francia."
texto = "Mientras programo, un pajaro ha saltado por el balcón y se ha comido una golondrina"
# Para esta, idenfica mal el CD ya que pone a Golondrina como sujeto


########################################################################################################################
########################################################################################################################
########################################################################################################################
#spacy_load = "es_core_news_lg"
#spacy_load = "es_core_news_sm"
spacy_load = "es_core_news_lg"

print("Texto: ", texto)
list_palabras, list_relaciones = get_list_palabras_relaciones(texto, spacy_load)








print("Palabras: ", list_palabras)
print("Relaciones: ", list_relaciones)
for pal in list_palabras:
    print(pal.to_create_Palabra_str())

for rel in list_relaciones:
    print(rel.to_create_Relacion_str())

Palabra.refresh_dict_palabras()

generate_graph(texto, list_palabras, list_relaciones)


