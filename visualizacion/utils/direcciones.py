import math
import random
import time

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, RegularPolygon, Ellipse, Rectangle

from utils.Grafo import Grafo
from utils.Palabra import Palabra
from utils.Relacion import Relacion

from constants.figuras import *
from constants.type_morfologico import *
from constants.type_sintax import *
from constants import type_sintax
from constants import colores_figura, colores_figura_letra, colores
from constants.figuras import *
from constants import tam_figuras

from utils.utils_text import unir_list_all_relaciones, unir_siglos_annos_all_list, unir_conjuncion_y, \
    truncate_a_8_relaciones

from constants.direcciones_relaciones import DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_ABAJO, DIR_ARRIBA, \
    DIR_IZQ, DIR_IZQ_ARRIBA, DIR_IZQ_ABAJO, FIND_DIR_CENTRO, FIND_DIR_DCHA, FIND_DIR_DCHA_ABAJO, FIND_DIR_DCHA_ARRIBA, \
    FIND_DIR_ABAJO, FIND_DIR_ARRIBA, FIND_DIR_IZQ, FIND_DIR_IZQ_ARRIBA, FIND_DIR_IZQ_ABAJO, DICT_DIR_BY_ORIGEN, CENTRO, \
    DICT_PROX_DIR, OPOSIT_DIR
from visualizacion.utils.posicionesXY import get_next_location, get_dir_relativa
from visualizacion.utils.matrix_functions import generate_matrix, get_pos_media_matrix, imprimir_matriz, \
    reducir_tam_matriz, ampliar_matriz

import logging
import os
from utils.logger import FORMAT_1
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL) #######################################################
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter(FORMAT_1)

# add formatter to ch
ch.setFormatter(formatter)
logger.addHandler(ch)
if (logger.hasHandlers()):
    logger.handlers.clear()

PAL_DEBUG = os.getenv('PAL_DEBUG', '')



def get_rel_origen_and_dest_unidas(palabra):
    list_relaciones_pal_origen = Palabra.relaciones_dict_origen.get(palabra, [])
    for rel in list_relaciones_pal_origen:
        rel.pal_tmp = rel.pal_dest
        rel.pal_tmp_opuesta = rel.pal_origen
    list_relaciones_pal_dest = Palabra.relaciones_dict_destino.get(palabra, [])
    for rel in list_relaciones_pal_dest:
        rel.pal_tmp = rel.pal_origen
        rel.pal_tmp_opuesta = rel.pal_dest
    list_relaciones_pal = list(set(list_relaciones_pal_origen + list_relaciones_pal_dest))
    # ordenar por el numero de grado de aproximacion
    list_relaciones_pal.sort(key=lambda x: x.pal_tmp.numero_grafos, reverse=True)
    # eliminar todas las que no esten en relations_pending
    list_relaciones_pal = [rel for rel in list_relaciones_pal if rel in palabra.relations_pending]
    return list_relaciones_pal



########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

def is_possible_in_dict(palabra, list_pos_to_plot, palabras_ptes_representar):
    num_pal_ptes_representar = len(palabras_ptes_representar)
    for pos in list_pos_to_plot:
        if palabra.dict_posiciones.get(pos) is None:
            num_pal_ptes_representar -= 1

    return num_pal_ptes_representar <= 0


def encajar_en_dict_direcciones(palabra, list_relaciones_pal, list_all_palabras, elements_comunes):
    if elements_comunes != []:
        encajar_en_dict_direcciones_con_elem_comunes(palabra, elements_comunes, list_relaciones_pal, list_all_palabras)

    # Y una vez guardados estos elementos, se guardan los que no tienen elementos comunes
    return encajar_en_dict_direcciones_sin_elem_comunes(palabra, list_relaciones_pal, list_all_palabras)


def encajar_en_dict_direcciones_con_elem_comunes(palabra, elements_comunes, list_relaciones_pal, list_all_palabras):
    txt = palabra.texto
    palabras_relaciones_proximas = palabra.palabras_relaciones_proximas.copy()

    list_palabras_pendientes = [a for a in list_all_palabras if a not in palabra.dict_posiciones.values()]

    is_possible = is_possible = list_palabras_pendientes == []  # si son == [], es que ya estan todas representadas
    number_to_search = len(list_relaciones_pal) - 1
    list_direcciones_orden = []
    find_dir_generic = DICT_DIR_BY_ORIGEN.get(palabra.direccion_origen_final, [])
    while not is_possible:
        if len(list_relaciones_pal) > len(find_dir_generic):
            # FIXME: en este caso lo ideal seria tener un diccionario secundario que aceptase otras 12 relaciones
            #  este diccionario seria solo con las de dcha_arriba, dcha_abajo, izq_arriba, izq_abajo (trasversales)
            #  (3 por cada direccion) y de esta forma caben todas en el grafo. Pero eso a futuro.
            list_direcciones_orden = find_dir_generic[-1]
            is_possible = True
        else:
            list_direcciones_orden = find_dir_generic[number_to_search]
            is_possible = is_possible_in_dict(palabra, list_direcciones_orden, palabras_relaciones_proximas)
        number_to_search += 1

    list_direcciones_orden = list_direcciones_orden.copy()
    for elem_comun in elements_comunes:
        if all([elem.has_been_plotted for elem in elem_comun]):
            continue
        if len(elem_comun) < 2:
            continue

        if any([elem.has_been_plotted for elem in elem_comun]):
            #TODO implementar esto, es decir, hay que buscar el elemento representado y construir los otros a partir de este
            pass
        dir_1 = list_direcciones_orden.pop(0)
        find_dir_prox = DICT_PROX_DIR.get(dir_1, [])
        list_dir_elem_prox = find_dir_prox[len(elem_comun) - 2]
        # si todos los elementos en palabra.dict_posiciones son Nulos, True
        if all([palabra.dict_posiciones.get(elem, None) is None for elem in list_dir_elem_prox]):
            # rellena esos elementos con un elem de elem_comun
            for elem in list_dir_elem_prox:
                palabra.dict_posiciones[elem] = elem_comun.pop(0)
                palabra.dict_posiciones[elem].direccion_origen_tmp = elem
                # si la posicion existe en list_direcciones_orden, la elimina
                if elem in list_direcciones_orden:
                    list_direcciones_orden.remove(elem)


    for list_pal_rel_prox in palabras_relaciones_proximas:
        # quitar todas las palabras que has_been_plotted
        list_pal_rel_prox = [elem for elem in list_pal_rel_prox if not elem.has_been_plotted]
        elemes_com = []
        # comprueba si dentro de esa lista existe alguna palabra en dict_posiciones
        # obtengo una lista de todos los valores no nulos de dict_posiciones
        # si alguno de los elementos de list_pal_rel_prox esta en dict_posiciones, True
        pos_elems_comunes = [elem in [a for a in list(palabra.dict_posiciones.values()) if a is not None]
                            for elem in list_pal_rel_prox]
        if any(pos_elems_comunes):
            # añado todas las posiciones que son True en elemn_comun
            elemes_com = [list_pal_rel_prox[i] for i, x in enumerate(pos_elems_comunes) if x]

        # Aqui obtengo la lista de direcciones siempre y cuando los elementos comunes estén ya guardaditos :)
        # comprobando que están entre esas direcciones y que tiene la dimension suficiente como para meter mi elemento.
        list_dir_elem_prox_final = []
        for i in range(len(DICT_PROX_DIR) - len(list_pal_rel_prox) - 1):
            # Esto lo que hace es ir buscando posiciones y, si no lo encuentra, a buscar con un grado de proximidad mayor
            # y asi sucesivamente hasta encontrar lo que se busca
            for elem_com in elemes_com:
                # Los elem_com ya estan representados
                find_dir_prox = DICT_PROX_DIR.get(elem_com.direccion_origen_tmp, [])
                list_dir_elem_prox = find_dir_prox[i + len(list_pal_rel_prox) - 2].copy()
                # si todos los elemes_com tienen direccion_origen dentro de la lista_dir_elem_prox, True
                if all([elem.direccion_origen_tmp in list_dir_elem_prox for elem in elemes_com]):
                    # Bien, los elementos comunes que quiero están representados.
                    # ahora debo comprobar si las posiciones restantes estan a None:
                    list_elems_dir = [elem for elem in list(palabra.dict_posiciones.keys()) if elem in list_dir_elem_prox]
                    # dime el numero de Trues que hay
                    num_trues = sum([palabra.dict_posiciones.get(key, None) is None for key in list_elems_dir])
                    if num_trues >= len(list_pal_rel_prox) - len(elemes_com):
                        # si esto es mayor, es que si cabe :)
                        list_dir_elem_prox_final = list_dir_elem_prox.copy()
                        # restar una lista a otra
                        list_pal_rel_prox = [a for a in list_pal_rel_prox if a not in elemes_com]
                        for pos in list_dir_elem_prox_final:
                            if palabra.dict_posiciones.get(pos, None) is None and list_pal_rel_prox != []:
                                palabra.dict_posiciones[pos] = list_pal_rel_prox.pop(0)
                                palabra.dict_posiciones[pos].direccion_origen_tmp = pos

                else:
                    continue
                if len(list_dir_elem_prox_final) > 0:
                    break
            if len(list_dir_elem_prox_final) > 0:
                break
    ###################################################################################################################


def encajar_en_dict_direcciones_sin_elem_comunes(palabra, list_relaciones_pal, list_all_palabras):
    txt = palabra.texto
    list_palabras_pendientes = [a for a in list_all_palabras if a not in palabra.dict_posiciones.values()]

    is_possible = list_palabras_pendientes == []  # si son == [], es que ya estan todas representadas
    number_to_search = len(list_palabras_pendientes) - 1
    list_direcciones_orden = []
    find_dir_generic = DICT_DIR_BY_ORIGEN.get(palabra.direccion_origen_final, [])
    while not is_possible:
        if len(list_relaciones_pal) > len(find_dir_generic):
            # FIXME: en este caso lo ideal seria tener un diccionario secundario que aceptase otras 12 relaciones
            #  este diccionario seria solo con las de dcha_arriba, dcha_abajo, izq_arriba, izq_abajo (trasversales)
            #  (3 por cada direccion) y de esta forma caben todas en el grafo. Pero eso a futuro.
            list_direcciones_orden = find_dir_generic[-1]
            is_possible = True
        else:
            list_direcciones_orden = find_dir_generic[number_to_search]
            is_possible = is_possible_in_dict(palabra, list_direcciones_orden, list_palabras_pendientes)
        number_to_search += 1

    # y en orden estricto de numero de relaciones, se rellena
    # ordenar la list_palabras_pendientes por el numero de grafos que tiene
    list_palabras_pendientes.sort(key=lambda x: x.numero_grafos, reverse=True)

    palabra.deprec_lista_direcciones_orden = list_direcciones_orden
    try:
        # obtener el elemento con menor importancia de list_relaciones_pal para ponerlo a la izq, si se puede
        ## pal_menor_import = min(list_palabras_pendientes, key=lambda x: x.importancia)

        for dir in list_direcciones_orden:
            if palabra.dict_posiciones.get(dir, None) is None and list_palabras_pendientes != []:
                palabra.dict_posiciones[dir] = list_palabras_pendientes.pop(0)
                palabra.dict_posiciones[dir].direccion_origen_tmp = dir

    except Exception as _:
        palabra.deprec_lista_direcciones_orden = find_dir_generic[-1]
        list_direcciones_orden = palabra.deprec_lista_direcciones_orden.copy()
        for dir in list_direcciones_orden:
            if palabra.dict_posiciones.get(dir, None) is None and list_palabras_pendientes != []:
                palabra.dict_posiciones[dir] = list_palabras_pendientes.pop(0)
                palabra.dict_posiciones[dir].direccion_origen_tmp = dir

    return True




# TODO una funcion de check if it is possible. para marcar estas relaciones
def refresh_directions(palabra):
    # TODO quitar de aqui todo lo que no se tenga que representar porque ya esta representado :)
    txt = palabra.texto
    if txt == PAL_DEBUG:
        print('debug')
    palabras_relaciones_proximas = palabra.palabras_relaciones_proximas.copy()
    # Esto crea las palabras temporales, es esencial
    list_relaciones_pal = get_rel_origen_and_dest_unidas(palabra).copy()
    list_all_palabras = [elem.pal_tmp for elem in list_relaciones_pal]
    # Guardar en el diccionario las palabras que ya existen y que estan representadas en el grafo.
    for pal2 in list_all_palabras:
        if pal2.has_been_plotted:
            dir_actual = get_dir_relativa(palabra, pal2)
            if palabra.dict_posiciones.get(dir_actual) is None:
                palabra.dict_posiciones[dir_actual] = pal2
            #pal2.direccion_origen_tmp = dir_actual


    # TODO: que busque la palabra con menor importancia y la ponga a la izq, si la izq esta vacia
    ## pal_menor_import = min(list_palabras_pendientes, key=lambda x: x.importancia)
    ######################################################################################################
    # si existe algun elemento de la 1a lista que esta en las otras, lo uno en elementos comunes para saber que deben ir juntos
    elements_comunes = deprec_get_list_elements_comunes(palabra, palabras_relaciones_proximas)

    encajar_en_dict_direcciones(palabra, list_relaciones_pal, list_all_palabras, elements_comunes)

    logger.info("Hola")


def deprec_get_list_elements_comunes(palabra, palabras_relaciones_proximas):
    palabras_relaciones_proximas = palabras_relaciones_proximas.copy()
    if len(palabras_relaciones_proximas) >= 2:
        i = 1
        new_palabras_relaciones_proximas = palabra.palabras_relaciones_proximas.copy()
        for elem in palabra.palabras_relaciones_proximas:
            for elem2 in palabra.palabras_relaciones_proximas[i:]:
                same_elem = False
                if len(elem) == len(elem2):
                    # toda palabra dentro de elem esta en elem2
                    # [True for pal1 in elem if pal1 in elem2 else False]
                    same_elem = all([True if pal1 in elem2 else False for pal1 in elem])
                    same_elem = same_elem and all([True if pal2 in elem else False for pal2 in elem2])
                    if same_elem and elem2 in new_palabras_relaciones_proximas:
                        new_palabras_relaciones_proximas.remove(elem2)
                if len(elem) > len(elem2):
                    same_elem = all([True if pal2 in elem else False for pal2 in elem2])
                    if same_elem and elem2 in new_palabras_relaciones_proximas:
                        new_palabras_relaciones_proximas.remove(elem2)
            i += 1
        palabras_relaciones_proximas = new_palabras_relaciones_proximas
    if len(palabras_relaciones_proximas) >= 2:
        i = 1
        new_palabras_relaciones_proximas_copy = palabras_relaciones_proximas.copy()
        #recorrer la lista al reves:
        for elem in palabras_relaciones_proximas[::-1]:
            list_reverse = palabras_relaciones_proximas[::-1]
            for elem2 in list_reverse[i:]:
                same_elem = False
                if len(elem) == len(elem2):
                    # toda palabra dentro de elem esta en elem2
                    same_elem = all([True if pal1 in elem2 else False for pal1 in elem])
                    same_elem = same_elem and all([True if pal2 in elem else False for pal2 in elem2])
                    if same_elem and elem2 in new_palabras_relaciones_proximas_copy:
                        new_palabras_relaciones_proximas_copy.remove(elem2)
                if len(elem) > len(elem2):
                    same_elem = all([True if pal2 in elem else False for pal2 in elem2])
                    if same_elem and elem2 in new_palabras_relaciones_proximas_copy:
                        new_palabras_relaciones_proximas_copy.remove(elem2)
            i += 1
        palabras_relaciones_proximas = new_palabras_relaciones_proximas_copy

    elements_comunes = []
    if len(palabras_relaciones_proximas) >= 2:
        i = 1
        for list_pals in palabras_relaciones_proximas:
            for list_pals_2 in palabras_relaciones_proximas[i:]:
                elem_comun = [elem in list_pals for elem in list_pals_2]
                if any(elem_comun) and list_pals != list_pals_2:
                    # añado todas las posiciones que son True en elemn_comun
                    elements_comunes.append([list_pals_2[i] for i, x in enumerate(elem_comun) if x])
                logger.info(elements_comunes)
    return elements_comunes
