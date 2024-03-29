"""
Con spicy NPL quiero pasarle una frase y que me saque las caracteristicas morg¡fologicas y sintacticas de cada palabra.
Tambien quiero que cree relaciones entre ellas.
"""
import re
import spacy
from unidecode import unidecode
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

from flask import Flask, request, jsonify
from flask_cors import CORS

from npl_module import token_manual_modifier
from utils.Grafo import Grafo
from utils.Palabra import Palabra
from utils.Relacion import Relacion
from constants.type_morfologico import *
from constants.type_sintax import *
from utils.TokenNLP import TokenNLP, TYPE_RELACION, TYPE_PALABRA
from utils.utils_text import son_pal_rel_contiguas
# from visualizacion.graficoFinal2 import print_graph
from visualizacion.grafico14 import print_graph, generate_graph

import sys
from io import StringIO



# python -m spacy download es_dep_news_trf




#LIST_TYPES_CONNECTOR_RELATION = [TYPE_MORF_ADP, TYPE_MORF_ADP, TYPE_MORF_CONJ, TYPE_MORF_CCONJ, TYPE_MORF_SCONJ,
#                                 TYPE_MORF_DET, TYPE_MORF_PRON, TYPE_MORF_PART, TYPE_MORF_VERB, TYPE_MORF_AUX]



#LIST_TYPES_SINTAX_RELATION = [TYPE_SINTAX_ADVMOD, TYPE_SINTAX_NPADVMOD]



def print_spacy_tree(doc):
    print()
    # Imprimir el árbol de dependencias sintácticas en formato de árbol
    for token in doc:
        print(token.text, token.dep_, token.head.text)

    def print_tree(token, level=0):
        print('\t' * level + f"{token.text} -- {token.dep_}")
        for child in token.children:
            print_tree(child, level + 1)

    root = [token for token in doc if token.head == token][0]
    print_tree(root)
    print()

def get_list_palabras_relaciones(texto):
    list_token_nlp_oraciones = preprocesing_oracion_nlp(texto)

    print("#### Tras preprocesamiento: ")
    imprimir_nuevos_tokens_nlp(list_token_nlp_oraciones)

    list_palabras = get_list_palabras(list_token_nlp_oraciones)
    list_relaciones = get_list_relaciones(list_palabras)
    manejar_palabras_restantes(list_token_nlp_oraciones)
    relaciones_root_vb_cambio_suj_vb(list_relaciones)

    return list_palabras, list_relaciones


def relaciones_root_vb_cambio_suj_vb(list_relaciones):
    # Modificar las relaciones para que, si ROOT es VB y la palDest es VERBO, se cambie la relación al Sujeto
    # Existe alguna relacion entre root y Sujeto
    sujeto = None
    for rel in list_relaciones:
        if rel.pal_dest.lugar_sintactico == TYPE_SINTAX_ROOT and rel.pal_origen.lugar_sintactico == TYPE_SINTAX_NSUBJ:
            sujeto = rel.pal_origen
            break
    if sujeto is not None:
        for rel in list_relaciones:
            if rel.pal_origen.lugar_sintactico == TYPE_SINTAX_ROOT and rel.pal_origen.tipo_morf == TYPE_MORF_VERB \
                    and rel.pal_dest.tipo_morf == TYPE_MORF_VERB and rel.pal_dest.lugar_sintactico not in LIST_SINTAX_TYPES_ROOT_VB_OK:
                rel.change_pal_origen(sujeto)


def manejar_palabras_restantes(list_token_nlp_oraciones):
    # Sacar las palabras que no se han sacado antes, omitiendo las Ys (que ya se verá como hacer enumeraciones después)
    # Y hay que comprobar que, si una palabra es igual a la que hay en la relación, no se ponga (en minusculas y sin acentos)
    for oracion in list_token_nlp_oraciones:
        for token in oracion:
            if token.representado or token.tipo_morfol == 'SPACE' or token.tipo_morfol == 'PUNCT':
                continue
            else:
                if token.tipo_morfol == TYPE_MORF_CCONJ:
                    continue
                if token.token_nlp_padre is not None:
                    pal_padre = token.token_nlp_padre.palabra_que_representa
                    if pal_padre is None:
                        pal_padre = token.palabra_padre_final
                    rel_dest_padre = Palabra.relaciones_dict_destino.get(pal_padre)
                    entontrada = False
                    if rel_dest_padre is not None and rel_dest_padre != []:
                        for rel in rel_dest_padre:
                            if rel.texto == token.text or rel.texto.__contains__(' ' + token.text + ' '):
                                entontrada = True
                                break
                    if entontrada:
                        continue
                    if pal_padre is not None and isinstance(pal_padre, Palabra):
                        # Si no esta en la relacion, se lo añado a la palabra, ya que no tiene relación hijo
                        pal_padre.add_aux_text(token.text, token.position_doc)

                print("hola")
                print(token)


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
            if token_nlp.tipo_morfol == 'SPACE' or token_nlp.tipo_morfol == 'PUNCT':
                continue
            if token_nlp.tipo_palabra is TYPE_PALABRA:
                if (token_nlp.tipo_morfol == 'AUX' and token_nlp.token_nlp_padre is not None and
                        token_nlp.token_nlp_padre.tipo_morfol == 'VERB'):
                    # Es el auxiliar de un verbo (ha saltado, se ha comido...)
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    if nueva_palabra is not None and isinstance(nueva_palabra, Palabra):
                        nueva_palabra.add_aux_text(token_nlp.text, token_nlp.position_doc)

                elif token_nlp.tipo_morfol == 'PRON' and token_nlp.lugar_sintact_original not in ('nsubj', 'obj') and \
                     token_nlp.token_nlp_padre is not None and token_nlp.token_nlp_padre.tipo_morfol == 'VERB':
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    if nueva_palabra is not None and isinstance(nueva_palabra, Palabra):
                        nueva_palabra.add_aux_text(token_nlp.text, token_nlp.position_doc)
                # En caso de que efectivamente sean pronombres que acompañen al verbo
                elif token_nlp.tipo_morfol == 'PRON' and token_nlp.lugar_sintact_original not in ('nsubj') and \
                     token_nlp.token_nlp_padre is not None and token_nlp.token_nlp_padre.tipo_morfol == 'VERB' and \
                        token_nlp.lema in ("yo", "tú", "él", "ella", "usted", "nosotros", "nosotras", "vosotros",
                                           "vosotras", "ellos", "ellas", "ustedes"):
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    if nueva_palabra is not None and isinstance(nueva_palabra, Palabra):
                        nueva_palabra.add_aux_text(token_nlp.text, token_nlp.position_doc)

                # Ahora el AUX que va con afjetivo, para "es impresionante"
                elif token_nlp.tipo_morfol == 'AUX' and token_nlp.lugar_sintact_original == 'cop' and \
                    token_nlp.token_nlp_padre is not None and token_nlp.token_nlp_padre.tipo_morfol in ('ADJ', 'NOUN'):
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    if nueva_palabra is not None and isinstance(nueva_palabra, Palabra):
                        nueva_palabra.add_aux_text(token_nlp.text, token_nlp.position_doc)

                # más rico, que vaya junto
                elif token_nlp.tipo_morfol == 'ADV' and token_nlp.lugar_sintact_original == 'advmod' and \
                     token_nlp.token_nlp_padre is not None and token_nlp.token_nlp_padre.tipo_morfol in ('ADJ', 'VERB'):
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    if nueva_palabra is not None and isinstance(nueva_palabra, Palabra):
                        nueva_palabra.add_aux_text(token_nlp.text, token_nlp.position_doc)
                #
                elif token_nlp.tipo_morfol == 'ADJ' and token_nlp.lugar_sintact_original == 'advmod' and \
                     token_nlp.token_nlp_padre is not None and token_nlp.token_nlp_padre.tipo_morfol in ('ADJ', 'NOUN'):
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    if nueva_palabra is not None and isinstance(nueva_palabra, Palabra):
                        nueva_palabra.add_aux_text(token_nlp.text, token_nlp.position_doc)

                # estudio informatica:
                elif token_nlp.tipo_morfol == 'ADJ' and token_nlp.token_nlp_padre is not None and \
                    token_nlp.token_nlp_padre.lugar_sintact_original in ('appos'):
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    if nueva_palabra is not None and isinstance(nueva_palabra, Palabra):
                        nueva_palabra.add_aux_text(token_nlp.text, token_nlp.position_doc)
                elif token_nlp.tipo_morfol == 'SCONJ' and token_nlp.token_nlp_padre is not None:
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    if nueva_palabra is not None and isinstance(nueva_palabra, Palabra):
                        nueva_palabra.add_aux_text(token_nlp.text, token_nlp.position_doc)
                elif token_nlp.lugar_sintact_original == TYPE_SINTAX_FLAT and token_nlp.token_nlp_padre is not None:
                    # Es el auxiliar de una palabra (Felipe II...)
                    nueva_palabra = token_nlp.token_nlp_padre.palabra_que_representa
                    if nueva_palabra is not None and isinstance(nueva_palabra, Palabra):
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



def completar_sujeto_omitido(oraciones, nlp):
    list_oraciones = []
    for oracion in oraciones.split('.'):
        doc = nlp(oracion)
        sujeto_omitido = None

        hay_sujeto = False
        for token in doc:
            if token.dep_ == "nsubj":
                hay_sujeto = True
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                sujeto_omitido = token
                break

        if sujeto_omitido is None and not hay_sujeto:
            for token in doc:
                if token.tag_ == 'PRON' and token.head.pos_ == "VERB":
                    sujeto_omitido = token
                    break

        if sujeto_omitido is not None and not hay_sujeto and sujeto_omitido.text != sujeto_omitido.lemma_:
            sujeto_completo = sujeto_omitido.lemma_
            list_oraciones.append(oracion.replace(sujeto_omitido.text, sujeto_completo + " " + sujeto_omitido.text))
        else:
            list_oraciones.append(oracion)

    return '. '.join(list_oraciones)


def hay_sujeto(doc):
    for token in doc:
        if token.dep_ == "nsubj":
            return True
    return False


def cambiar_root_nombre_propio(doc):
    # Igual es porque el ROOT es el sujeto y no el verbo principal.
    # Ocurre con los nombres propios, si ent_type es persona, debo cambiarlo
    root = None
    encontrado = False
    for token in doc:
        if token.dep_ == "ROOT" and token.ent_type_ == 'PER':
            root = token
            break
    if root is None:
        return doc, False

    for chile_root in root.children:
        if chile_root.dep_ == "ROOT" and chile_root.ent_type_ == "PERSON":
            chile_root.dep_ = "nsubj"
            encontrado = False
            break
    return doc, encontrado



def preprocesing_oracion_nlp(texto):
    texto = texto.replace('\n', '. ').replace('\r', '. ').replace('\t', '. ').\
        replace("    ", " ").replace("   ", " ").replace("  ", " ")

    encontrado = False
    doc = None
    nlp = None
    list_spacy_loads = ['es_dep_news_trf', 'es_core_news_lg', 'es_core_news_md', 'es_core_news_sm', 'es_dep_news_trf']
    while not encontrado and list_spacy_loads != []:
        spacy_load = list_spacy_loads.pop(0)
        nlp = spacy.load(spacy_load)
        texto = completar_sujeto_omitido(texto, nlp)
        doc = nlp(texto)
        print("Spacy load: ", spacy_load)
        print("Resultado sin procesar: ")
        imprimir_doc(doc)
        #print_spacy_tree(doc)

        # Cambiar los ROOT personales por sujetos y los verbos principales por ROOT con sus relaciones.
        if not hay_sujeto(doc):
            doc, encontrado = cambiar_root_nombre_propio(doc)
        else:
            encontrado = True

    print("#### Resultado añadiendo sujeto omitido: ")
    imprimir_doc(doc)

    spacy_patrones(doc, nlp)

    print("#### Resultado añadiendo patrones (CCL, CCT): ")
    imprimir_doc(doc)

    ## Primero lo divido en oraciones
    list_token_oraciones = []
    list_token_nlp_oraciones = []
    list_oracion_actual = []

    get_list_token_oraciones(doc, list_oracion_actual, list_token_oraciones)

    print("#### Obtenida nueva clase Token mia: ")
    imprimir_nuevos_tokens_nlp(list_token_oraciones)

    # Después, recorro la oración empezando por el Root
    num_oracion = -1
    for list_token_oracion in list_token_oraciones:
        num_oracion += 1
        list_token_nlp = []

        print("Oracion: ", num_oracion)
        # Ordenar la lista de tokens de la oracion por el número de children
        list_token_oracion.sort(key=lambda x: len(list(x.children)), reverse=True)
        list_token_oracion = [token for token in list_token_oracion if token.pos_ not in ('SPACE', 'PUNCT') ]

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
            if token.text not in list_texts_ok and not (token.pos_ == TYPE_MORF_PUNCT and token.lemma_ == '.')\
                    and not (token.pos_ == 'SPACE'):
                list_token_nlp_2 = analyse_token_recursive(None, token, num_oracion)
                list_token_nlp = list_token_nlp + list_token_nlp_2

        for token_nlp in list_token_nlp:
            token_nlp.refresh_parents_children()
        # quitar todos los tokens que sean de tipo puntuacion
        list_token_nlp = [token_nlp for token_nlp in list_token_nlp if token_nlp.tipo_morfol != TYPE_MORF_PUNCT]
        list_token_nlp_oraciones.append(list_token_nlp)

    return list_token_nlp_oraciones


def spacy_patrones(doc, nlp):
    # Definir los patrones de coincidencia
    # Ref: https://www.ejemplos.co/ejemplos-de-adverbios-de-tiempo/
    adverbsCCT = [
        "actualmente", "enseguida", "normalmente", "ahora", "entretanto", "nunca", "anoche", "eternamente",
        "ocasionalmente", "anteriormente", "finalmente", "posteriormente", "antes", "frecuentemente", "primeramente",
        "antiguamente", "hoy", "pronto", "asiduamente", "inicialmente", "puntualmente", "aún", "inmediatamente",
        "recién", "ayer", "instantáneamente", "recientemente", "constantemente", "jamás", "siempre",
        "contemporáneamente", "luego", "simultáneamente", "cuando", "mañana", "tarde", "desde", "mientras",
        "temprano", "después", "momentáneamente", "ya", "día", "días", "dia", "dias", "semana", "semanas", "mes",
        "meses",
        "aun","recien", "instantaneamente", "contemporaneamente", "cuando", "despues", "momentaneamente"
    ]
    unicode_adverbsCCT = [unidecode(adverbCCT) for adverbCCT in adverbsCCT]

    patterns = [[{"LOWER": adverbCCT}] for adverbCCT in adverbsCCT+unicode_adverbsCCT]

    matcher = Matcher(nlp.vocab)
    matcher.add("Time_Patterns", patterns)

    matches = matcher(doc)

    for match_id, start, end in matches:
        matched_span = doc[start:end]
        print("CCT: ", matched_span.text)
        for token in matched_span:
            if token.dep_ in LIST_SINTAX_PATTERN_MODIFY:
                #print("Old token:")
                #print(token.text, ": ", token.idx, token.lemma_, "|| pos_:", token.pos_, "|| tag_:", token.tag_,
                #      "|| dep_:", token.dep_, "|| ent_type_:", token.ent_type_, "|| ", token.shape_, token.is_alpha,
                #      token.is_stop)
                token.dep_ = TYPE_SINTAX_PATTERN_CCT
                #print("New token:")
                #print(token.text, ": ", token.idx, token.lemma_, "|| pos_:", token.pos_, "|| tag_:", token.tag_,
                #      "|| dep_:", token.dep_, "|| ent_type_:", token.ent_type_, "|| ", token.shape_, token.is_alpha,
                #      token.is_stop)

    ######################################################
    ######################################################
    # REF: https://www.ejemplos.co/25-ejemplos-de-adverbios-de-lugar/
    adverbsCCL = [
        "a través", "aquí", "donde", "abajo", "arriba", "en",
        "acá", "atrás", "encima", "afuera", "bajo", "enfrente",
        "ahí", "cerca", "entre", "al borde", "delante", "junto a",
        "allá", "dentro", "lejos de", "allí", "desde", "por debajo",
        "alrededor", "detrás", "sobre",
        "a traves", "aqui", "aca", "atras", "ahi", "alla", "alli", "detras"
    ]
    unicode_adverbsCCL = [unidecode(adverbCCL) for adverbCCL in adverbsCCL]
    patterns = [[{"LOWER": unidecode(adverbCCL)}] for adverbCCL in adverbsCCL + unicode_adverbsCCL]

    matcher = Matcher(nlp.vocab)
    matcher.add("Time_Patterns", patterns)

    matches = matcher(doc)

    for match_id, start, end in matches:
        matched_span = doc[start:end]
        print("CCL: ", matched_span.text)
        for token in matched_span:
            if token.dep_ in LIST_SINTAX_PATTERN_MODIFY:
                print("Old token:")
                print(token.text, ": ", token.idx, token.lemma_, "|| pos_:", token.pos_, "|| tag_:", token.tag_,
                      "|| dep_:", token.dep_, "|| ent_type_:", token.ent_type_, "|| ", token.shape_, token.is_alpha,
                      token.is_stop)
                token.dep_ = TYPE_SINTAX_PATTERN_CCL
                print("New token:")
                print(token.text, ": ", token.idx, token.lemma_, "|| pos_:", token.pos_, "|| tag_:", token.tag_,
                      "|| dep_:", token.dep_, "|| ent_type_:", token.ent_type_, "|| ", token.shape_, token.is_alpha,
                      token.is_stop)


def imprimir_doc(doc):
    for token in doc:
        ########################################
        print(token.text, ": ", token.idx, token.lemma_, "|| pos_:", token.pos_, "|| tag_:", token.tag_,
              "|| dep_:", token.dep_, "|| ent_type_:", token.ent_type_, "|| ", token.shape_, token.is_alpha, token.is_stop)
        for child in token.children:
            print("-->child:", child)
    print()
    print()
def imprimir_nuevos_tokens_nlp(list_token_oraciones):
    for oracion in list_token_oraciones:
        for token in oracion:
            ########################################
            if isinstance(token, TokenNLP):
                print(token.text, ": ", token.position_doc, token.lema, "|| pos_:", token.tipo_morfol, "|| tag_:", token.token_tag,
                      "|| dep_:", token.lugar_sintact_original, "|| ent_type_:", token.ent_type)
                for child_nlp in token.list_children_nlp:
                    print("-->child:", child_nlp.text)
            else:
                print(token.text, ": ", token.idx, token.lemma_, "|| pos_:", token.pos_, "|| tag_:", token.tag_,
                      "|| dep_:", token.dep_, "|| ent_type_:", token.ent_type_, "|| ", token.shape_, token.is_alpha,
                      token.is_stop)
                for child in token.children:
                    print("-->child:", child)
    print()
    print()




def get_list_token_oraciones(doc, list_oracion_actual, list_token_oraciones):
    for token in doc:
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


texto = "Isthar come paja en el pajar mientras Jasper le mira mientras Tina caza palomas para cenar"
#texto = "Mi perro y mi gato juegan juntos en el parque con una pelota"
#texto = "Me llamo Rubén y tengo 25 años. Vivo en Madrid y trabajo en una empresa de tecnología. Me gusta leer, viajar y pasar tiempo con mi familia y amigos."
#texto = "Los Austrias gobernaron España en el siglo XVI y XVII, responsables también de la Inquisición, expulsión de judíos. Su legado: arquitectura y arte en Madrid y Córdoba."
#texto = "Ruben cocina hamburguesas en la Freidora de aire"
#texto = "La naturaleza es impresionante en su variedad de paisajes, desde montañas majestuosas y extensas llanuras hasta océanos y ríos caudalosos."

###################################################################################################
##### TEST Flat
texto = "Felipe II fué rey de españa hace tiempo. Maria Antonieta era reina de Francia."
texto = "Mientras programo, un pajaro ha saltado por el balcón y se ha comido una golondrina"
# Para esta, idenfica mal el CD ya que pone a Golondrina como sujeto
# el SmallModel si calcula bien que es 'obj', es decir, CD.
#texto = "La naturaleza es impresionante en su variedad de paisajes"
###################################################################################################

#### TEST Root-VB a SUJ-VB
texto = "El perro de mi vecino se llama Toby y sale a jugar al parque todos los días"
texto = "Me llamo Ruben, estudio informatica y espero poder acabar el master algún día"
texto = "Me llamo Ruben, estudio informatica y soy de Madrid"


#### TEST Sujeto omitido
texto = "Me voy a jugar al futbol"
texto = "El otro día me llamaron de una empresa nueva"
texto = "Mi perro es un golden retriever de tres años que adora jugar con su pelota en el parque y siempre me da la bienvenida moviendo la cola cuando llego a casa."


# conflictivo con muchos sujetos omitidos, a ver cómo saco las relaciones de aqui.
texto = "Pedro se compró un coche nuevo la semana pasada porque el suyo, que tenía ya 10 años, se rompió"


########################################################################################################################
########################################################################################################################
########################################################################################################################
#texto = "Ruben cocina hamburguesas en la Freidora de aire ayer"


#texto = "Yo le añadí un poco de cilantro a la pasta para que supiera más rica. Tras esto, la quemé"
#texto = "Rubén le regaló juguetes a Okami por su cumpleaños. Pero ella los rompió en dos minutos."
# TODO que el DOS vaya dentro del rectangulo
#  Que el 'a Okami' lo pille como CI y no directo


#spacy_load = "es_core_news_lg"
#spacy_load = "es_core_news_sm"
#spacy_load = "es_core_news_md"
#spacy_load = "es_core_news_lg"
# NLTK, AllenNLP y StanfordNLP

txt_prints = ""
def ejecutar_texto(texto):
    # Crear un objeto StringIO para redirigir la salida
    string_io = StringIO()
    #sys.stdout = string_io
    global txt_prints

    num_intentos = 0
    ok_exec = False
    while not ok_exec and num_intentos < 20:
        try:
            list_palabras, list_relaciones = get_list_palabras_relaciones(texto)
            if list_palabras is None or list_palabras == []:
                return "No se ha recibido texto"

            #print("Palabras: ", list_palabras)
            #print("Relaciones: ", list_relaciones)
            for pal in list_palabras:
                print(pal.to_create_Palabra_str())

            print()
            for rel in list_relaciones:
                print(rel.to_create_Relacion_str())

            Palabra.refresh_dict_palabras()

            # Obtener el contenido del string

            txt_prints = string_io.getvalue()
            print(txt_prints)
            # Restaurar la salida estándar
            sys.stdout = sys.__stdout__

            fig = generate_graph(texto, list_palabras, list_relaciones)
            if fig is not None:
                ok_exec = True
        except Exception as e:
            print("Error: ", e)
            ok_exec = False
        num_intentos += 1



########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

#ejecutar_texto(texto)

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

app = Flask(__name__)
CORS(app)
################################################

def obtener_prints_python():
    global txt_prints
    return jsonify(texto=txt_prints)


def recibir_texto():
    borrar_imagenes_2()
    texto = request.json['texto']

    import os
    os.environ['PRINT_MATRIX'] = 'False'
    os.environ['PRINT_IMG'] = 'False'
    os.environ['PRINT_GRAPH'] = 'False'
    os.environ['ZOOM_ACTIVE'] = 'False'


    if texto is None or texto == "":
        return "No se ha recibido texto"

    # Aquí puedes realizar cualquier procesamiento o análisis del texto que desees
    print("Texto: ", texto)
    ejecutar_texto(texto)
    # El otro día me llamaron de una empresa nueva

    Palabra.id_actual = 9
    Palabra.palabras_dict = {}
    Palabra.palabras_dict_id = {}
    Palabra.relaciones_dict_origen = {}
    Palabra.relaciones_dict_destino = {}
    Relacion.id_actual = -9
    Relacion.relaciones_dict = {}
    Relacion.relaciones_dict_id = {}
    Grafo.id_actual = 0
    TokenNLP.nlp_token_dict = {}

    return 'Texto recibido: {}'.format(texto)


def borrar_imagenes():
    # Funcion desactivada ya que se le llama desde JS y no es necesario
    pass
def borrar_imagenes_2():
    import os
    ruta_imagenes = 'web_project/imagenes/'  # Ruta de la carpeta donde se encuentran las imágenes

    # Eliminar todas las imágenes en la ruta especificada
    for filename in os.listdir(ruta_imagenes):
        file_path = os.path.join(ruta_imagenes, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return 'Imágenes borradas exitosamente'



def lambda_handler(event, context):
    #TODO
    print(event)
    print(context)
    ejecutar_texto(texto)

ejecutar_texto(texto)