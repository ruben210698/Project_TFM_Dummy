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
# from visualizacion.graficoFinal2 import print_graph
from visualizacion.grafico12 import print_graph

# python -m spacy download es_core_news_sm
nlp = spacy.load("es_core_news_sm")
#nlp = spacy.load("es_core_news_md")
# El que mejor lo hace, el primero considera "dibuja" adjetivo -.- y el segundo "rie" adjetivo tambien.
#nlp = spacy.load("es_core_news_lg")

list_types_connector_relation = [TYPE_MORF_ADP, TYPE_MORF_ADP, TYPE_MORF_CONJ, TYPE_MORF_CCONJ, TYPE_MORF_SCONJ,
                                 TYPE_MORF_DET, TYPE_MORF_PRON, TYPE_MORF_PART, TYPE_MORF_VERB]


def get_relation(rel, fifo_heads, fifo_children):
    possible_relations = []
    for key in fifo_heads:
        if key.pos_ == TYPE_MORF_PUNCT:
            continue
        list_value = fifo_heads[key]
        for pal in list_value:
            if isinstance(pal, Token) and pal == rel and key not in possible_relations and \
                    Palabra.palabras_dict.get(key.lemma_, None) is not None: # es decir, que existe una palabra y no es una relacion
                possible_relations.append(key)

    for key in fifo_children:
        if key.pos_ == TYPE_MORF_PUNCT:
            continue
        list_value = fifo_children[key]
        for pal in list_value:
            if isinstance(pal, Token) and pal == rel and key not in possible_relations and \
                    Palabra.palabras_dict.get(key.lemma_, None) is not None: # es decir, que existe una palabra y no es una relacion
                possible_relations.append(key)

    # Obtener los heads de las palabras relacionadas. Asi engordar la lista de posibles relaciones
    # Solo 1er grado, por eso solo hay un bucle y se hace una copia de la lista.
    possible_relations_copy = possible_relations.copy()
    for pal in possible_relations_copy:
        if pal.head is not None and pal.head != rel and pal.head not in possible_relations:
            possible_relations.append(pal.head)
        for child in pal.children:
            if child not in possible_relations and child != rel:
                possible_relations.append(child)

    return possible_relations

def get_list_palabras_relaciones(texto,spacy_load):
    nlp = spacy.load(spacy_load)
    list_palabras =  []
    list_relaciones = []
    list_tokens_rel = []

    # Primero los objetos y luego las relaciones.
    doc = nlp(texto)
    fifo_heads = {}
    fifo_children = {}
    for token in doc:
        token = token_manual_modifier.set_token_manual(token)
        print(token.text, ": ", token.idx, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

        texto_palabra = token.text
        tipo_morfol = token.pos_
        lugar_sintact = token.dep_
        lema_palabra = token.lemma_
        position_doc = token.idx

        if tipo_morfol == TYPE_MORF_PUNCT:
            continue
        # Crear objeto Palabra y añadir a lista de palabras
        nueva_palabra = token
        if tipo_morfol not in list_types_connector_relation:
            nueva_palabra = Palabra.get_palabra_by_lema(lema_palabra, position_doc)
            if nueva_palabra is None:
                nueva_palabra = Palabra(texto_palabra, tipo_morfol, lugar_sintact, txt_lema=lema_palabra,
                                        position_doc=position_doc)
            list_palabras.append(nueva_palabra)
        else:
            list_tokens_rel.append(token)

        if token.head is not None and token.head != token:
            if token.head not in fifo_heads.keys():
                fifo_heads.update({token.head: [nueva_palabra]})
            else:
                fifo_heads[token.head].append(nueva_palabra)

        for child in token.children:
            print(child)
            if child not in fifo_children.keys():
                fifo_children.update({child: [nueva_palabra]})
            else:
                fifo_children[child].append(nueva_palabra)



    doc = nlp(texto)
    dict_relations_1_2 = {}



    for relation in list_tokens_rel:
        print(relation)
        fifo_heads_copy = fifo_heads.get(relation, [])

        relation_possible_list = None
        if fifo_heads_copy == []:
            relation_possible_list = get_relation(relation, fifo_heads, fifo_children)
            for rel_possibl in relation_possible_list:
                palabra = Palabra.palabras_dict.get(rel_possibl.lemma_, None)
                if palabra is not None:
                    fifo_heads_copy.append(palabra)

        # ver si alguna palabra head es token y en caso de serlo, buscar si existe palabra relacionada.
        if fifo_heads_copy is not None and fifo_heads_copy != []:
            fifo_heads_copy = fifo_heads_copy.copy()
            relacion1 = None
            relacion2 = None
            position_doc = relation.idx
            #position_rel = relation.pos

            for pal in fifo_heads.get(relation, []):
                if isinstance(pal, Token):
                    #TODO para el futuro, de momento se quita y ya
                    for i in range(len(fifo_heads_copy)-1, -1, -1): #recorrerlo al reves para hacer bien el POP
                        if isinstance(fifo_heads_copy[i], Token) and fifo_heads_copy[i] == pal:
                            fifo_heads_copy.pop(i)

            if len(fifo_heads_copy) <= 1:
                relation_possible_list_new = get_relation(relation, fifo_heads, fifo_children)
                for rel_possibl in relation_possible_list_new:
                    palabra = Palabra.palabras_dict.get(rel_possibl.lemma_, None)
                    if palabra is not None and palabra not in fifo_heads_copy:
                        fifo_heads_copy.append(palabra)

            if len(fifo_heads_copy) <= 1:
                # No hay relaciones posibles
                continue

            # Ordena y determinar relacionPal1.
            relacion1 = fifo_heads_copy[0]
            for pal in fifo_heads_copy:
                if isinstance(pal, Palabra) and pal.position_doc < relacion1.position_doc:
                    relacion1 = pal
            fifo_heads_copy.remove(relacion1)

            for pal_rel_2 in fifo_heads_copy:
                nueva_relacion = Relacion(
                    texto=relation.text,
                    pal_origen=relacion1,
                    pal_dest=pal_rel_2,
                    position_doc=position_doc,
                    lugar_sintactico=pal_rel_2.lugar_sintactico)
                list_relaciones.append(nueva_relacion)
                dict_relations_1_2.update({relacion1: pal_rel_2})

    return list_palabras, list_relaciones


#texto = "Ruben dibuja koalas en bañador y chanclas"


texto = "Ruben dibuja koalas en bañador saltando entre acantilados mientras su amigo graba la escena y se rie."
texto = "Okami jugó en el parque con palos"
texto = "Ruben cocina hamburguesas en la Freidora de aire"
texto = "Ruben cocina hamburguesas con carne picada y cebolla en la sartén que tiene el aceite hirviendo"
texto = "La dinastía de los Austrias gobernó España desde el siglo XVI hasta el siglo XVII. Durante su reinado, el país " \
        "experimentó una época de esplendor y decadencia. Los monarcas austriacos, entre ellos Carlos I y Felipe II, " \
        "ampliaron el territorio español mediante la conquista de América y la anexión de Portugal. Sin embargo, también " \
        "fueron responsables de la Inquisición española y de la expulsión de los judíos. La falta de recursos y las guerras " \
        "en Europa contribuyeron al declive de la monarquía, que terminó con la llegada de la dinastía de los Borbones " \
        "en el siglo XVIII. El legado de los Austrias en España se puede ver en su arquitectura y arte, especialmente en " \
        "Madrid y en las ciudades andaluzas de Granada y Córdoba."

texto = "Los Austrias gobernaron España en el siglo XVI y XVII, ampliando su territorio pero también responsables de la Inquisición y la expulsión de judíos. Su legado se ve en la arquitectura y el arte, especialmente en Madrid, Granada y Córdoba."
texto = "Los Austrias gobernaron España en el siglo XVI y XVII, responsables también de la Inquisición, expulsión de judíos. Su legado: arquitectura y arte en Madrid, Córdoba."
texto = "Los Austrias gobernaron España en el siglo XVI, responsables también de la Inquisición"

#spacy_load ="es_core_news_sm"
#spacy_load = "es_core_news_md
spacy_load = "es_core_news_lg"
spacy_load = "es_core_news_sm"

list_palabras, list_relaciones = get_list_palabras_relaciones(texto, spacy_load)
#mirar la lista de relaciones_dict_dest y origen y ver si alguna palabra de la list_palabras no tiene ninguna
# relacion con ninguna otra palabra. Si es asi, añadir a lista_palabras_sin_relacion
lista_palabras_sin_relacion = []
for palabra in list_palabras:
    if palabra not in Palabra.relaciones_dict_origen.keys() and palabra not in Palabra.relaciones_dict_destino.keys():
        lista_palabras_sin_relacion.append(palabra)
lista_palabras_sin_aparicion = texto.split(" ")
for palabra in list_palabras:
    if palabra.texto in lista_palabras_sin_aparicion:
        lista_palabras_sin_aparicion.remove(palabra.texto)
for relacion in list_relaciones:
    if relacion.texto in lista_palabras_sin_aparicion:
        lista_palabras_sin_aparicion.remove(relacion.texto)
print(lista_palabras_sin_aparicion)


spacy_load = "es_core_news_sm"
spacy_load = "es_core_news_lg"
list_palabras2, list_relaciones2 = get_list_palabras_relaciones(texto, spacy_load)

# hay alguna de las palabras de list_palabras2 que no esten en list_palabras_sin_aparicion?
list_palabras2_copy = list_palabras2.copy()
for palabra in list_palabras2:
    if palabra.texto not in lista_palabras_sin_aparicion:
        list_palabras2_copy.remove(palabra)
print(list_palabras2_copy)

list_relaciones2_copy = list_relaciones2.copy()
for relacion in list_relaciones2:
    if relacion.texto not in lista_palabras_sin_aparicion:
        list_relaciones2_copy.remove(relacion)
print(list_relaciones2_copy)

#TODO, no se qué hacer, si aceptar todas las relaciones o solo la primera de cada tipo (es decir, texto)
def remove_repeated_relations(list_relaciones):
    # Elimina desde la ultima
    # pero dejando una de ellas y comparandola con el texto
    list_relaciones_copy = list_relaciones.copy()
    # lista con solo los textos de las relaciones
    list_textos = [rel.texto for rel in list_relaciones]
    for i in range(len(list_relaciones)-1, -1, -1):
        relacion = list_relaciones[i]
        if relacion.texto in list_textos[:i]:
            list_relaciones_copy.remove(relacion)
    return list_relaciones_copy

list_palabras = list_palabras + list_palabras2_copy
list_relaciones = list_relaciones + remove_repeated_relations(list_relaciones2_copy)

print("Palabras: ", list_palabras)
print("Relaciones: ", list_relaciones)
for pal in list_palabras:
    print(pal.to_create_Palabra_str())

for rel in list_relaciones:
    print(rel.to_create_Relacion_str())

print_graph(texto, list_palabras, list_relaciones)


# if token in fifo_heads.keys():
#     rel_pal_origen = fifo_heads[token]
#     print("Es el padre de ", fifo_heads[token].texto)
#     # TODO hacer algo especial si es verbo.
#
#     new_relation = \
#         Relacion(nueva_palabra.texto, pal_origen=rel_pal_origen, pal_dest=None)
#     list_relaciones.append(new_relation)



















    # para obtener el padre sintactico, debo buscar token.head. En Ruben dibuja Koalas, el padre de Ruben es "dibuja"
    # TODO: para los verbos quiero hacer algo más especial. Que se pongan en un simbolo pero con flechas vacias a los lados.
    #  pero que si es un verbo final (Ruben se rie), que se ponga una flecha retroalimentandose o algo asi.

    # TODO: la conunción Y. o mirar como hacer lo de la conjuncion. Tiene que coger la misma relacion que la palabra
    #  anterior y ponerla en la palabra actual

    # Si la palabra tiene un padre sintáctico, crear objeto Relacion y añadir a lista de relaciones
    # if token.head != token:
    #     texto_relacion = token.head.text
    #     lugar_sintactico_relacion = token.dep_
    #     pal_origen = nueva_palabra
    #     pal_dest = Palabra.palabras_dict[texto_relacion]
    #     nueva_relacion = Relacion(texto_relacion, pal_origen, pal_dest, lugar_sintactico_relacion)
    #     list_relaciones.append(nueva_relacion)





"""

texto3 = "ruben dibuja koalas en bañador saltando entre acantilados mientras su amigo graba la escena y se rie."

list_palabras = []
list_palabras.append(Palabra("ruben", NOMBRE, SUJETO, importancia=1))
list_palabras.append(Palabra("koalas", NOMBRE, CD, importancia=2))
list_palabras.append(Palabra("bañador", NOMBRE, CCL, importancia=2))
list_palabras.append(Palabra("acantilados", NOMBRE, CCL, importancia=2))
list_palabras.append(Palabra("amigo", NOMBRE, CCCOMP, importancia=3))
list_palabras.append(Palabra("escena", NOMBRE, CD, importancia=3))
list_palabras.append(Palabra("rie", VERBO, PREDICADO, importancia=3))

list_relaciones = []
list_relaciones.append(Relacion("dibuja", pal_origen=palabras_dict["ruben"], pal_dest=palabras_dict["koalas"], lugar_sintactico=PREDICADO, importancia=2))
list_relaciones.append(Relacion("en", pal_origen=palabras_dict["koalas"], pal_dest=palabras_dict["bañador"], lugar_sintactico=CCL, importancia=2))
list_relaciones.append(Relacion("saltando", pal_origen=palabras_dict["koalas"], pal_dest=palabras_dict["acantilados"], lugar_sintactico=CCL, importancia=2))
list_relaciones.append(Relacion("mientras", pal_origen=palabras_dict["ruben"], pal_dest=palabras_dict["amigo"], lugar_sintactico=CCCOMP, importancia=3))
list_relaciones.append(Relacion("graba", pal_origen=palabras_dict["amigo"], pal_dest=palabras_dict["escena"], lugar_sintactico=CD, importancia=3))
list_relaciones.append(Relacion("", pal_origen=palabras_dict["amigo"], pal_dest=palabras_dict["rie"], lugar_sintactico=PREDICADO, importancia=3))

"""