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
    FIND_DIR_ABAJO, FIND_DIR_ARRIBA, FIND_DIR_IZQ, FIND_DIR_IZQ_ARRIBA, FIND_DIR_IZQ_ABAJO, DICT_DIR_BY_ORIGEN, CENTRO
from visualizacion.utils.direcciones import get_next_location
from visualizacion.utils.matrix_functions import generate_matrix, get_pos_media_matrix, imprimir_matriz, \
    reducir_tam_matriz, ampliar_matriz

LINEAS_SEP_FILA = 5

PRINT_GRAPH = False

MODE_DEBUG = "DEBUG"
MODE_NORMAL = "NORMAL"
EX_MODE = MODE_DEBUG

dict_color_figura = {
    getattr(type_sintax, nombre_variable): valor_variable
    for nombre_variable, valor_variable in vars(colores_figura).items()
    if nombre_variable.startswith("TYPE_SINTAX_")
}
dict_color_figura.update({None: colores.default, "": colores.default})

dict_color_figura_letra = {
    getattr(type_sintax, nombre_variable): valor_variable
    for nombre_variable, valor_variable in vars(colores_figura_letra).items()
    if nombre_variable.startswith("TYPE_SINTAX_")
}
dict_color_figura_letra.update({None: colores.default, "": colores.default})


"""
¿Qué necesito aqui?
Pues necesito que me saque las relaciones entre palabras. Es decir, la flecha, el verbo que necesitaré.
También tengo que saber qué tipo de palabra es.
Saber a qué hace referencia para poner bien el color.
Enlazar palabras con imágenes.

Gráficamente:
- Tengo que hacer que dinámicamente se vayan añadiendo palabras y que me las distribuya bien en el lienzo.


Web:
- Varios botones, o mejor uno de + y otro de - para ir agregando nivel de detalle en diferentes colores.
Esto simplemente lo que haría sería ir cambiando la imagen a una más compleja o menos (dejar precargada de antes
mientras ves la primera imagen).

Siguientes pasos Grafico:
ok- Que acepte relaciones a la izquierda (es decir, que la matriz empiece en la mitad y no en 0
- Que acepte más de 4 relaciones. Es decir, que para abajo me deje poner una de longitud 4 y otra en diagonal de lng 2 :) Y asi acepta 8.
- Que al buscar un hueco para poner la flecha busque que haya un hueco de 5 elementos a la dcha. Si no,
que suba otros 2. O que baje otros 2. O que vaya 5 más a la izq.

Futuro Avanzado:
- Una opcion que sea a modo arbol genealogico. Es decir, en vez de a la cha, que vaya hacia abajo
- Que cuando las relaciones sean 2, se queden bonitas con un angulo de 45º. Si son 3, con un angulo de 30º. Y no putos cuadrados.
"""


# TODO:
#  Que se añada el numero de relaciones de cada palabra y de esa forma se pueda calcular la importancia de cada palabra
#  y la posicion en la que colocarla y en la que colocar las demás.
#  - Añadir 1s cuando la relación vaya a pasar por ahi en la matriz.


# Función para dibujar aristas con flechas
def draw_edge(ax, u, v, width=1.0, color='k', label='', label_offset=(0, 0), bold=False):
    arrow = FancyArrowPatch(u, v, arrowstyle='->', mutation_scale=20, linewidth=width, color=color)
    ax.add_patch(arrow)
    if label:
        x_label = (u[0] + v[0]) / 2 + label_offset[0]
        y_label = (u[1] + v[1]) / 2 + label_offset[1]
        if bold:
            ax.text(x_label, y_label, label, fontsize=12, ha='center', va='center', zorder=3, weight='bold')
        else:
            ax.text(x_label, y_label, label, fontsize=12, ha='center', va='center', zorder=3)


def get_importance_dict(list_palabras):
    new_dict = {}
    for pal in list_palabras:
        new_dict[pal] = {"importancia": pal.importancia, "dimension": pal.dimension}
    # ordenar el diccionario por importancia
    new_dict = dict(sorted(new_dict.items(), key=lambda item: item[1]["importancia"]))

    return new_dict




def loop_reducir_posiciones_finales_eje_y(posiciones_finales, cambiado):
    ultima_y_leida = 0
    dim_y_reducir = 0
    i = -1
    posiciones_finales_loop = posiciones_finales.copy()
    cambiado = False
    for palabra, posicion in posiciones_finales_loop.items():
        i += 1
        pos_y_actual = posicion[1]
        if (pos_y_actual - ultima_y_leida) > 5:
            dim_y_reducir += (pos_y_actual - ultima_y_leida - 5)
        if dim_y_reducir > 0:
            nueva_pos_y = pos_y_actual - dim_y_reducir
            posiciones_finales.update({palabra: (posicion[0], nueva_pos_y)})
            cambiado = True
        ultima_y_leida = pos_y_actual
    return posiciones_finales, cambiado


def reducir_posiciones_finales_eje_y(posiciones_finales):
    posiciones_finales = posiciones_finales.copy()
    # TODO lo que hace esta funcion es
    # 1. ordena de menor a mayor todos los elementos y
    # 2. mira si entre 1 y otro de alguno hay más de 10 elementos (recurda que están ordenados de menor a mayor)
    # 3. si existe, cojo las posiciones finales iniciales y reduzco esa diferencia "excesiva" a todas las ys
    #  de todos los elementos que estén por encima de ese numero :)

    # tengo que crear un diccionario de {palabra: {pos_x: pos_y}}
    # y que ordene por pos_y en orden.

    posiciones_finales = dict(sorted(posiciones_finales.items(), key=lambda x: x[1][1]))

    cambiado = False
    posiciones_finales, cambiado = loop_reducir_posiciones_finales_eje_y(posiciones_finales, cambiado)

    while cambiado == True:
        posiciones_finales, cambiado = loop_reducir_posiciones_finales_eje_y(posiciones_finales, cambiado)

    return posiciones_finales



def loop_reducir_posiciones_finales_eje_x(posiciones_finales, cambiado):
    ultima_x_leida = 0
    dim_x_reducir = 0
    i = -1
    posiciones_finales_loop = posiciones_finales.copy()
    cambiado = False
    for palabra, posicion in posiciones_finales_loop.items():
        i += 1
        pos_x_actual = posicion[0]
        if (pos_x_actual - ultima_x_leida) > 15:
            dim_x_reducir += (pos_x_actual - ultima_x_leida - 15)
        if dim_x_reducir > 0:
            nueva_pos_x = pos_x_actual - dim_x_reducir
            posiciones_finales.update({palabra: (nueva_pos_x, posicion[1])})
            cambiado = True
        ultima_x_leida = pos_x_actual
    return posiciones_finales, cambiado


def reducir_posiciones_finales_eje_x(posiciones_finales):
    posiciones_finales = posiciones_finales.copy()
    # TODO lo que hace esta funcion es
    # 1. ordena de menor a mayor todos los elementos y
    # 2. mira si entre 1 y otro de alguno hay más de 10 elementos (recurda que están ordenados de menor a mayor)
    # 3. si existe, cojo las posiciones finales iniciales y reduzco esa diferencia "excesiva" a todas las ys
    #  de todos los elementos que estén por encima de ese numero :)

    # tengo que crear un diccionario de {palabra: {pos_x: pos_y}}
    # y que ordene por pos_y en orden.

    posiciones_finales = dict(sorted(posiciones_finales.items(), key=lambda x: x[1][0]))

    cambiado = False
    posiciones_finales, cambiado = loop_reducir_posiciones_finales_eje_x(posiciones_finales, cambiado)

    while cambiado == True:
        posiciones_finales, cambiado = loop_reducir_posiciones_finales_eje_x(posiciones_finales, cambiado)

    return posiciones_finales


def update_relations_in_matrix_by_pal(matrix_dim, palabra):
    pos_y_media, pos_x_media = get_pos_media_matrix(matrix_dim)
    list_rel = Palabra.relaciones_dict_origen.get(palabra) + Palabra.relaciones_dict_destino.get(palabra)
    for rel in list_rel:
        id = rel.id
        print(palabra.texto)
        imprimir_matriz(matrix_dim)
        if not rel.has_been_plotted:
            pal_origen = rel.pal_origen
            pal_dest = rel.pal_dest
            x_origen = pal_origen.pos_x
            x_dest = pal_dest.pos_x
            y_origen = pal_origen.pos_y
            y_dest = pal_dest.pos_y
            if x_origen is None or x_dest is None or y_origen is None or y_dest is None:
                continue

            x_origen += pos_x_media
            x_dest += pos_x_media
            y_origen += pos_y_media
            y_dest += pos_y_media

            y = min(y_origen, y_dest)
            x = min(x_origen, x_dest)
            x_repres = x
            y_repres = y

            if (x_dest - x_origen) == 0: # ARRIBA O ABAJO
                while y_repres < max(y_origen, y_dest):
                    try:
                        if matrix_dim[y_repres][x_repres] == 0:
                            matrix_dim[y_repres][x_repres] = id
                        y_repres += 1
                    except Exception as _:
                        matrix_dim = ampliar_matriz(matrix_dim)
                        pos_y_media_old, pos_x_media_old = pos_y_media, pos_x_media
                        y_origen_old, x_origen_old = y_origen, x_origen
                        y_dest_old, x_dest_old = y_dest, x_dest
                        pos_y_media, pos_x_media = get_pos_media_matrix(matrix_dim)
                        y_repres = y_repres - pos_y_media_old + pos_y_media
                        x_repres = x_repres - pos_x_media_old + pos_x_media
                        y_origen = y_origen - pos_y_media_old + pos_y_media
                        y_dest = y_dest - pos_y_media_old + pos_y_media
                        x_origen = x_origen - pos_x_media_old + pos_x_media
                        x_dest = x_dest - pos_x_media_old + pos_x_media
                continue

            if (y_dest - y_origen) == 0:  # DCHA O IZQ
                while x_repres < max(x_origen, x_dest):
                    try:
                        if matrix_dim[y_repres][x_repres] == 0:
                            matrix_dim[y_repres][x_repres] = id
                        x_repres += 1
                    except Exception as _:
                        matrix_dim = ampliar_matriz(matrix_dim)
                        pos_y_media_old, pos_x_media_old = pos_y_media, pos_x_media
                        y_origen_old, x_origen_old = y_origen, x_origen
                        pos_y_media, pos_x_media = get_pos_media_matrix(matrix_dim)
                        y_repres = y_repres - pos_y_media_old + pos_y_media
                        x_repres = x_repres - pos_x_media_old + pos_x_media

                        y_origen = y_origen - y_origen_old + pos_y_media
                        y_dest = y_dest - pos_y_media_old + pos_y_media
                        x_origen = x_origen - pos_x_media_old + pos_x_media
                        x_dest = x_dest - pos_x_media_old + pos_x_media
                continue

            m = (y_dest - y_origen) / (x_dest - x_origen)
            #if m > 0: # DCHA_ARRIBA o IZQ_ABAJO # DCHA_ABAJO o IZQ_ARRIBA
            i = 1
            while x_repres < max(x_origen, x_dest) and y_repres < max(y_origen, y_dest):
                try:
                    x_repres = int(x + i)
                    y_repres = int(y + i * m)
                    if matrix_dim[y_repres][x_repres] == 0:
                        matrix_dim[y_repres][x_repres] = id
                    i += 1
                except Exception as _:
                    matrix_dim = ampliar_matriz(matrix_dim)
                    pos_y_media_old, pos_x_media_old = pos_y_media, pos_x_media
                    y_origen_old, x_origen_old = y_origen, x_origen
                    y_dest_old, x_dest_old = y_dest, x_dest
                    pos_y_media, pos_x_media = get_pos_media_matrix(matrix_dim)
                    y_repres = y_repres - pos_y_media_old + pos_y_media
                    x_repres = x_repres - pos_x_media_old + pos_x_media
                    y_origen = y_origen - pos_y_media_old + pos_y_media
                    y_dest = y_dest - pos_y_media_old + pos_y_media
                    x_origen = x_origen - pos_x_media_old + pos_x_media
                    x_dest = x_dest - pos_x_media_old + pos_x_media

            #if m < 0: # DCHA_ABAJO o IZQ_ARRIBA


            rel.has_been_plotted = True
        else:
            continue
    print(palabra.texto)
    imprimir_matriz(matrix_dim)



    return matrix_dim


def update_palabras_in_matrix(matrix_dim, palabra):
    pos_y_media, pos_x_media = get_pos_media_matrix(matrix_dim)
    axis_y = palabra.pos_y + pos_y_media
    axis_x = palabra.pos_x + pos_x_media
    # bucle que recorre palabra.dimension_y desde -palabra.dimension_y//2 hasta palabra.dimension_y//2
    for y in range(palabra.dimension_y):
        axis_y_loop = axis_y + y - palabra.dimension_y // 2
        matrix_dim[axis_y_loop][axis_x:axis_x + palabra.dimension + palabra.cte_sum_x] = \
            [palabra.id for x in range(palabra.dimension + 2)]

    matrix_dim = update_relations_in_matrix_by_pal(matrix_dim, palabra)
    return matrix_dim


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


def represent_list_relations(list_palabras_representadas, list_relaciones, matrix_dim, palabra, position_elems,
                             force_draw=False):
    list_relaciones_pal = get_rel_origen_and_dest_unidas(palabra)

    list_direcciones_orden = []
    if len(list_relaciones_pal) > 0:
        list_relaciones_pal.sort(
            key=lambda x: x.pal_tmp.grafos_aproximados[0] if len(x.pal_tmp.grafos_aproximados) > 0 else 0,
            reverse=True)
        find_dir = DICT_DIR_BY_ORIGEN.get(palabra.direccion_origen)
        # FIXME: meter aqui un try-except por si supera 7 elementos.
        if len(list_relaciones_pal) > len(find_dir):
            list_direcciones_orden = find_dir[-1]
        else:
            list_direcciones_orden = find_dir[len(list_relaciones_pal) - 1]
        palabra.lista_direcciones_orden = list_direcciones_orden

    # TODO esto que hace???????
    list_relaciones_pal = DEPREC_reordenar_relaciones_unir_graph_1er_grado(list_relaciones_pal)
    if force_draw:
        list_relaciones_pal = get_rel_origen_and_dest_unidas(palabra)
        list_rel_pending = list(list_relaciones_pal)
        list_rel_pending = [rel for rel in list_rel_pending if not rel.pal_tmp.subgrafo_completado]
    else:
        list_relaciones_pal = get_rel_origen_and_dest_unidas(palabra)
        list_rel_pending = [a for a in list_relaciones_pal if a in palabra.relations_pending]

    num_dir_orden = -1
    num_relacion = -1
    while list_rel_pending != []:
        num_dir_orden += 1
        num_relacion += 1
        relation = list_rel_pending.pop(0)
        palabra.pos_actual_recorrer_dir_relaciones = num_dir_orden
        if check_subgrafo_completado(palabra):
            continue

        if relation.pal_tmp.has_been_plotted:
            # al coger un numero random evitamos que se formen bucles infinitos
            relation = list_relaciones_pal[random.randint(0, len(list_relaciones_pal) - 1)]
            list_palabras_representadas_new, position_elems_2, matrix_dim_2 = \
                get_position_word_recursive(position_elems, matrix_dim, relation.pal_tmp, list_relaciones,
                                            relation=relation, force_draw=force_draw)
            if palabra.grafo.palabras_list_ordered_num_rel_pending == []:
                break
        else:
            dir_actual = list_direcciones_orden[num_dir_orden]
            relation.direccion_actual = dir_actual
            relation.pal_tmp.direccion_origen = dir_actual

            print_graph(list_palabras_representadas, list_relaciones, position_elems, matrix_dim)
            if palabra.texto == 'majestuosas y extensas':
                print("hola")

            list_palabras_representadas_new, position_elems_2, matrix_dim_2 = \
                get_position_word_recursive(position_elems, matrix_dim, relation.pal_tmp, list_relaciones,
                                            relation=relation, force_draw=force_draw)

        if list_palabras_representadas_new is None or position_elems is None or matrix_dim is None:
            print("No se ha podido representar el grafo")
            list_direcciones_orden = palabra.lista_direcciones_orden
            list_palabras_representadas_new = []
            list_rel_pending.insert(0, relation)
        else:
            position_elems = position_elems_2
            matrix_dim = matrix_dim_2

        list_palabras_representadas += list_palabras_representadas_new
    return list_palabras_representadas, matrix_dim, position_elems



def represent_word(matrix_dim, palabra, relation, position_elems):
    axis_y, axis_x, matrix_dim = get_next_location(matrix_dim, palabra, relation)
    if axis_y is None or axis_x is None:
        print("No se ha podido representar la palabra: ", palabra.texto)
        return matrix_dim, None, relation, position_elems
    pos_y_media, pos_x_media = get_pos_media_matrix(matrix_dim)
    palabra.pos_y = axis_y - pos_y_media
    palabra.pos_x = axis_x - pos_x_media
    position_elems.update({
        palabra: (
            axis_x - pos_x_media,
            axis_y - pos_y_media
        )})

    # reemplazar los 0s por IDs para range(value['dimension']+2)
    matrix_dim = update_palabras_in_matrix(matrix_dim, palabra)

    imprimir_matriz(matrix_dim)
    palabra.has_been_plotted = True
    check_subgrafo_completado(palabra)

    return matrix_dim, palabra, relation, position_elems


def DEPREC_reordenar_relaciones_unir_graph_1er_grado(list_relaciones):
    # TODO sustituir por las listas de elementos contiguos que he creado para la palabra.
    # Busca las relaciones conflictivas de 2o grado y deja juntas las relaciones que pueden tener relaciones conflicitvas
    list_relaciones = list_relaciones.copy()
    dict_relaciones_2o_grado_conflictivas = {}
    list_pal_1er_grado = [a.pal_tmp for a in list_relaciones]
    for pal_2o_grado in list_pal_1er_grado:
        rel_orig_2o_grado = Palabra.relaciones_dict_origen.get(pal_2o_grado, [])
        re_dest_2o_grado = Palabra.relaciones_dict_destino.get(pal_2o_grado, [])
        rel_2o_grado = list(set(rel_orig_2o_grado + re_dest_2o_grado))
        for rel in rel_2o_grado:
            if rel in rel_orig_2o_grado and rel not in list_relaciones:
                rel.pal_tmp = rel.pal_dest
            elif rel in re_dest_2o_grado and rel not in list_relaciones:
                rel.pal_tmp = rel.pal_origen

            if rel.pal_tmp in list_pal_1er_grado and pal_2o_grado not in dict_relaciones_2o_grado_conflictivas.keys():
                dict_relaciones_2o_grado_conflictivas.update({pal_2o_grado: rel.pal_tmp})
    list_relaciones_copy = list_relaciones.copy()
    for pal1, pal2 in dict_relaciones_2o_grado_conflictivas.items():
        for rel in list_relaciones_copy:
            if rel.pal_tmp == pal1 or rel.pal_tmp == pal2:
                list_relaciones.remove(rel)
                list_relaciones.insert(0, rel)
    return list_relaciones

def check_subgrafo_completado(palabra):
    list_palabras_dest = [pal.pal_dest for pal in Palabra.relaciones_dict_origen.get(palabra, [])]
    if list_palabras_dest == [] and palabra.has_been_plotted:
        palabra.subgrafo_completado = True
        return True
    for pal_dest in list_palabras_dest:
        if not pal_dest.subgrafo_completado:
            return False
    return True


def get_position_word_recursive(position_elems, matrix_dim, palabra, list_relaciones, relation=None,
                                force_draw=False):
    list_palabras_representadas = []
    print(f"Matrix: {palabra.texto}")
    aaaaaaaaaaa = palabra.texto
    if palabra.texto == 'caudalosos':
        print("hola")

    draw_relations = not palabra.has_been_plotted_relations
    if not palabra.has_been_plotted and palabra.grafo.palabras_list_ordered_num_rel_pending != [] and \
        palabra.grafo.palabras_list_ordered_num_rel_pending[0] != palabra and draw_relations:
        draw_relations = False
    if not palabra.has_been_plotted and force_draw and palabra.grafo.palabras_list_ordered_num_rel_pending != [] and \
        palabra.grafo.palabras_list_ordered_num_rel_pending[0] == palabra:
        # En este caso, es esta palabra la que hay que dibujar con sus relaciones, asi que no hay que seguir forzando
        # el buscar la siguiente palabra
        draw_relations = True
        force_draw = False

    # time.sleep(10)
    ################################################################################################
    if not palabra.has_been_plotted:
        matrix_dim, palabra, relation, position_elems = \
            represent_word(matrix_dim, palabra, relation, position_elems)
        if palabra is None:
            return None, None, None
    ################################################################################################
    if force_draw or draw_relations:
        list_palabras_representadas, matrix_dim, position_elems = \
            represent_list_relations(list_palabras_representadas, list_relaciones, matrix_dim, palabra, position_elems,
                                     force_draw)
    ################################################################################################
    if palabra not in list_palabras_representadas:
        list_palabras_representadas.append(palabra)

    # TODO peta cuando le quedan 2
    if palabra.grafo.palabras_list_ordered_num_rel_pending != [] and \
        palabra.grafo.palabras_list_ordered_num_rel_pending[0] == palabra:
        palabra.grafo.palabras_list_ordered_num_rel_pending.pop(0)
        palabra.grafo.palabras_drawn.append(palabra)

    if draw_relations:
        palabra.has_been_plotted_relations = True

    return list_palabras_representadas, position_elems, matrix_dim



def get_next_word_to_repres(palabra_old):
    palabra_old.grafo.reordenar_pal_pending()
    for pal_pending in palabra_old.grafo.palabras_list_ordered_num_rel_pending:
        list_relaciones_pal = get_rel_origen_and_dest_unidas(pal_pending)
        for rel in list_relaciones_pal:
            if rel.pal_origen in palabra_old.grafo.palabras_drawn or \
                    rel.pal_dest in palabra_old.grafo.palabras_drawn:
                return pal_pending
    return None

def get_position_dict(list_palabras, list_relaciones):
    importance_dict = get_importance_dict(list_palabras)
    matrix_dim, pos_y_media, pos_x_media = generate_matrix(list_palabras)

    position_elems = {}
    dict_rel_direction = {}

    #list_palabras_ordenadas = list(importance_dict.keys())
    list_palabras_ordenadas = list_palabras.copy()
    list_palabras_ordenadas.sort(key=lambda x: x.numero_grafos, reverse=True)
    while len(list_palabras_ordenadas) != 0:
        palabra = list_palabras_ordenadas.pop(0)

        list_palabras_representadas, position_elems, matrix_dim = \
            get_position_word_recursive(position_elems, matrix_dim, palabra, list_relaciones, force_draw = False)

        try:
            while palabra is not None and \
                    (not palabra.grafo.is_all_drawn() or palabra.grafo.palabras_list_ordered_num_rel_pending == []):
                list_palabras_representadas, position_elems, matrix_dim = \
                    get_position_word_recursive(position_elems, matrix_dim, palabra, list_relaciones, force_draw=True)
                list_palabras_ordenadas.sort(key=lambda x: x.numero_grafos, reverse=True)
                palabra = get_next_word_to_repres(palabra)

                print_graph(list_palabras_representadas, list_relaciones, position_elems, matrix_dim)
                # quitar de list_palabras_ordenadas las palabras que ya han sido representadas
                list_palabras_ordenadas = [pal for pal in list_palabras_ordenadas if pal not in list_palabras_representadas]
                list_palabras_ordenadas.sort(key=lambda x: x.numero_grafos, reverse=True)

        except Exception as _:
            print("hola")

        print_graph(list_palabras, list_relaciones, position_elems, matrix_dim)

    position_elems = reducir_posiciones_finales_eje_y(position_elems)
    position_elems = reducir_posiciones_finales_eje_x(position_elems)

    return position_elems, matrix_dim


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def insertar_grafos_aproximados_palabras(list_palabras):
    for i in range(len(list_palabras) - 1, -1, -1):
        list_palabras[i].refresh_grafos_aproximados()


def remove_relations_without_words(list_relaciones):
    # Añadir nodos y aristas
    list_relaciones_to_remove = []
    for relation in list_relaciones:
        if relation.pal_origen is None or relation.pal_dest is None:
            list_relaciones_to_remove.append(relation)

    for relation in list_relaciones_to_remove:
        list_relaciones.remove(relation)
        relation.delete_relation()
    return list_relaciones


def generate_graphs(list_palabras):
    list_palabras_copy = list_palabras.copy()
    while list_palabras_copy != []:
        palabra_origen = list_palabras_copy.pop(0)
        list_palabras_copy = generate_graphs_recursive(palabra_origen, list_palabras_copy)

def generate_graphs_recursive(palabra_origen, list_palabras_copy):
    list_rel_origen = Palabra.relaciones_dict_origen[palabra_origen]
    list_rel_dest = Palabra.relaciones_dict_destino[palabra_origen]
    list_pal_1er_grado_origen = [rel.pal_dest for rel in list_rel_origen]
    list_pal_1er_grado_dest = [rel.pal_origen for rel in list_rel_dest]
    list_pal_1er_grado = list(set(list_pal_1er_grado_origen + list_pal_1er_grado_dest))
    for pal_1er_grado in list_pal_1er_grado:
        if pal_1er_grado.grafo is not None:
            palabra_origen.grafo = pal_1er_grado.grafo
            palabra_origen.grafo.add_node(palabra_origen)
            break
    if palabra_origen.grafo is None:
        # No hay ningun grafo al que añadir la palabra
        grafo = Grafo(palabra_origen)
        palabra_origen.grafo = grafo

    for pal_1er_grado in list_pal_1er_grado:
        if not list_palabras_copy.count(pal_1er_grado) > 0:
            continue
        list_palabras_copy.remove(pal_1er_grado)
        list_palabras_copy = generate_graphs_recursive(pal_1er_grado, list_palabras_copy)

    return list_palabras_copy





def text_tranformations(list_palabras, list_relaciones):
    list_palabras, list_relaciones = unir_conjuncion_y(list_palabras, list_relaciones)
    list_relaciones = unir_list_all_relaciones(list_relaciones)
    list_palabras, list_relaciones = unir_siglos_annos_all_list(list_palabras, list_relaciones)
    list_relaciones = unir_list_all_relaciones(list_relaciones)
    list_relaciones = remove_relations_without_words(list_relaciones)

    # al final:
    insertar_grafos_aproximados_palabras(list_palabras)
    truncate_a_8_relaciones(list_palabras)
    insertar_grafos_aproximados_palabras(list_palabras)
    generate_graphs(list_palabras)
    for palabra in list_palabras:
        palabra.refresh_pal_relations()
    for palabra in list_palabras:
        palabra.refresh_palabras_relacionadas_2o_grado()
    for palabra in list_palabras:
        palabra.refresh_relaciones_proximas_1er_grado()
    # TODO una funcion que a la primera palabra, las relaciones de esa palabra y las palabras de las relaciones las
    # ponga de color rojo, al siguiente nivel, azul, ect. Pero con el orden que da el grafo con relaciones de 1er grado
    #

    return list_palabras, list_relaciones


def generate_graph(texto, list_palabras, list_relaciones):
    list_palabras, list_relaciones = text_tranformations(list_palabras, list_relaciones)

    # Crear un grafo dirigido
    G = nx.DiGraph()
    for relation in list_relaciones:
        G.add_edge(relation.pal_origen, relation.pal_dest)

    # Crear posiciones de nodos
    position_elems, matrix_dim = get_position_dict(list_palabras, list_relaciones)

    print_graph(list_palabras, list_relaciones, position_elems, matrix_dim, final=True)

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

def print_graph(list_palabras, list_relaciones, position_elems, matrix_dim, final=False):
    if PRINT_GRAPH or final:
        _print_graph(list_palabras, list_relaciones, position_elems, matrix_dim)

def _print_graph(list_palabras, list_relaciones, position_elems, matrix_dim):
    position_elems = position_elems.copy()

    imprimir_matriz(matrix_dim, apply_num_inicial_col=False)
    matrix_dim_reduced = matrix_dim.copy()
    matrix_dim_reduced = reducir_tam_matriz(matrix_dim_reduced)

    imprimir_matriz(matrix_dim_reduced, apply_num_inicial_col=False)

    max_axis_y = max([x[1] for x in position_elems.values()]) + 3
    min_axis_y = min([x[1] for x in position_elems.values()]) - 3
    max_axis_x = max([x[0] for x in position_elems.values()]) + 5
    min_axis_x = min([x[0] for x in position_elems.values()]) - 5

    dif_y = abs(max_axis_y - min_axis_y)//2 - abs(max_axis_y - min_axis_y)//5
    dif_x = abs(max_axis_x - min_axis_x)//2 - abs(max_axis_x - min_axis_x)//5

    fig, ax = plt.subplots(figsize=(dif_x, dif_y))
    #fig, ax = plt.subplots(figsize=(24, 16))
    #fig, ax = plt.subplots()

    # Dibujar nodos
    draw_all_nodes(ax, position_elems)

    # Dibujar aristas
    draw_all_edges(ax, list_relaciones, position_elems)

    # draw_edge(ax, position_elems_deprec["ruben"], position_elems_deprec["pescado"], color=light_blue, label='come', label_offset=(0, 0.1))
    # draw_edge(ax, position_elems_deprec["pescado"], position_elems_deprec["restaurante"], color=light_blue, label='en', label_offset=(0, 0.1))
    # draw_edge(ax, position_elems_deprec["restaurante"], position_elems_deprec["pepe"], color=green, label='de', label_offset=(0, 0.1))

    # Configurar límites y aspecto del gráfico
    ax.set_ylim(min_axis_y, max_axis_y)
    ax.set_xlim(min_axis_x, max_axis_x)
    ax.set_aspect('equal')
    ax.axis('on')

    plt.show()

def calcular_direccion_aprox(relation_draw, position_elems):
    print("-- Calcular Dir Aprox: ", relation_draw.texto)
    print("Calcular Dir Aprox origen: ", relation_draw.pal_origen)
    print("Calcular Dir Aprox dest: ", relation_draw.pal_dest)
    pal_origen = relation_draw.pal_origen
    pal_dest = relation_draw.pal_dest
    coord_pal_origen = position_elems[pal_origen]
    coord_pal_dest = position_elems[pal_dest]
    x_origen_draw = coord_pal_origen[0]
    x_dest_draw = coord_pal_dest[0]
    y_origen_draw = coord_pal_origen[1]
    y_dest_draw = coord_pal_dest[1]
    if x_origen_draw == x_dest_draw and y_origen_draw < y_dest_draw:
        return DIR_ARRIBA
    elif x_origen_draw == x_dest_draw and y_origen_draw > y_dest_draw:
        return DIR_ABAJO
    elif x_origen_draw < x_dest_draw and y_origen_draw == y_dest_draw:
        return DIR_DCHA
    elif x_origen_draw > x_dest_draw and y_origen_draw == y_dest_draw:
        return DIR_IZQ
    elif x_origen_draw < x_dest_draw and y_origen_draw < y_dest_draw:
        return DIR_DCHA_ARRIBA
    elif x_origen_draw < x_dest_draw and y_origen_draw > y_dest_draw:
        return DIR_DCHA_ABAJO
    elif x_origen_draw > x_dest_draw and y_origen_draw < y_dest_draw:
        return DIR_IZQ_ARRIBA
    elif x_origen_draw > x_dest_draw and y_origen_draw > y_dest_draw:
        return DIR_IZQ_ABAJO
    else:
        return None


def draw_all_edges(ax, list_relaciones, position_elems):
    for relation_draw in list_relaciones:
        txt_rel = relation_draw.texto
        color = dict_color_figura.get(relation_draw.lugar_sintactico, dict_color_figura[None])
        x_origen_draw = 0
        x_dest_draw = 0
        if relation_draw.pal_origen.multiplicador_borde_figura is None:
            relation_draw.pal_origen.multiplicador_borde_figura = 0
        if relation_draw.pal_dest.multiplicador_borde_figura is None:
            relation_draw.pal_dest.multiplicador_borde_figura = 0

        try:
            pal_origen = relation_draw.pal_origen
            pal_dest = relation_draw.pal_dest
            coord_pal_origen = position_elems[pal_origen]
            coord_pal_dest = position_elems[pal_dest]

            x_origen_draw = coord_pal_origen[0]
            x_dest_draw = coord_pal_dest[0]
            y_origen_draw = coord_pal_origen[1]
            y_dest_draw = coord_pal_dest[1]

            if relation_draw.direccion_actual == None:
                #TODO quitar:
                #continue
                relation_draw.direccion_actual = calcular_direccion_aprox(relation_draw, position_elems)

            if relation_draw.direccion_actual == DIR_DCHA:
                x_dest_draw = coord_pal_dest[0] - pal_dest.multiplicador_borde_figura
            elif relation_draw.direccion_actual == DIR_IZQ:
                x_dest_draw = coord_pal_dest[0] + pal_dest.multiplicador_borde_figura
            elif relation_draw.direccion_actual == DIR_ARRIBA:
                y_dest_draw = coord_pal_dest[1] - pal_dest.tam_eje_y_figura
                x_dest_draw = coord_pal_dest[0]
            elif relation_draw.direccion_actual == DIR_ABAJO:
                y_dest_draw = coord_pal_dest[1] + pal_dest.tam_eje_y_figura
                x_dest_draw = coord_pal_dest[0]
            elif relation_draw.direccion_actual == DIR_DCHA_ARRIBA:
                x_dest_draw = coord_pal_dest[0] - pal_dest.multiplicador_borde_figura
                y_dest_draw = coord_pal_dest[1] - pal_dest.tam_eje_y_figura
            elif relation_draw.direccion_actual == DIR_DCHA_ABAJO:
                x_dest_draw = coord_pal_dest[0] - pal_dest.multiplicador_borde_figura
                y_dest_draw = coord_pal_dest[1] + pal_dest.tam_eje_y_figura
            elif relation_draw.direccion_actual == DIR_IZQ_ARRIBA:
                x_dest_draw = coord_pal_dest[0] + pal_dest.multiplicador_borde_figura
                y_dest_draw = coord_pal_dest[1] - pal_dest.tam_eje_y_figura
            elif relation_draw.direccion_actual == DIR_IZQ_ABAJO:
                x_dest_draw = coord_pal_dest[0] + pal_dest.multiplicador_borde_figura
                y_dest_draw = coord_pal_dest[1] + pal_dest.tam_eje_y_figura
            else:
                # TODO: que si no tiene direccion_actual, la calcule :)
                print("Error: dirección no contemplada", relation_draw.texto)
                print("###########")

            draw_edge(
                ax,
                (x_origen_draw, y_origen_draw),
                (x_dest_draw, y_dest_draw),
                color=color,
                label=relation_draw.texto,
                label_offset=(0, 0.4)
            )
        except Exception as e:
            print("Error al dibujar la relación", e)


def draw_all_nodes(ax, position_elems):
    for pal, (x, y) in position_elems.items():
        node_text = pal.texto
        print(pal.texto)
        if pal.lugar_sintactico.lower() in (TYPE_SINTAX_ROOT):
            pal.figura = FIGURA_ELIPSE
            pal.tam_eje_y_figura = tam_figuras.ELIPSE[1]
            pal.multiplicador_borde_figura = tam_figuras.ELIPSE[0] * len(node_text)
            ellipse_width = 0.6 * len(node_text)
            ellipse = Ellipse((x, y), width=ellipse_width, height=1,
                              color=dict_color_figura.get(pal.lugar_sintactico, colores.default), zorder=2)
            ax.add_patch(ellipse)
            ax.text(x, y, node_text, fontsize=12, ha='center', va='center', zorder=3,
                    color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))

        elif pal.lugar_sintactico.lower() in (TYPE_SINTAX_AMOD, TYPE_SINTAX_NMOD):
            pal.figura = FIGURA_RECTANGULO
            pal.tam_eje_y_figura = tam_figuras.RECTANGULO[1]
            pal.multiplicador_borde_figura = tam_figuras.RECTANGULO[0] * len(node_text)
            rectangle_width = tam_figuras.RECTANGULO[0] * 2 * len(node_text)
            rectangle = Rectangle((x - rectangle_width / 2, y - 0.4), width=rectangle_width, height=1,
                                  color=dict_color_figura.get(pal.lugar_sintactico, colores.default), zorder=2)
            ax.add_patch(rectangle)
            ax.text(x, y, node_text, fontsize=12, ha='center', va='center', zorder=3,
                    color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))
        #
        elif pal.lugar_sintactico.lower() in (TYPE_SINTAX_FLAT):
            pal.figura = FIGURA_HEXAGONO
            pal.tam_eje_y_figura = tam_figuras.HEXAGONO[1] * len(node_text)
            pal.multiplicador_borde_figura = tam_figuras.HEXAGONO[0] * len(node_text)
            polygon_radius = 0.4 * len(node_text)
            polygon = RegularPolygon((x, y), numVertices=6, radius=polygon_radius, orientation=0,
                                     color=dict_color_figura.get(pal.lugar_sintactico, colores.default), zorder=2)
            ax.add_patch(polygon)
            ax.text(x, y, node_text, fontsize=12, ha='center', va='center', zorder=3,
                    color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))
        #
        elif pal.lugar_sintactico.lower() in ():
            pal.figura = FIGURA_RECTANGULO
            pal.tam_eje_y_figura = tam_figuras.RECTANGULO[1]
            pal.multiplicador_borde_figura = tam_figuras.RECTANGULO[0] * len(node_text)
            # TODO
            rectangle_width = 0.1 * len(node_text) + 0.2
            rectangle = Rectangle((x - rectangle_width / 2, y - 0.25), width=rectangle_width, height=0.5,
                                  color=dict_color_figura.get(pal.lugar_sintactico, colores.default),
                                  zorder=2)
            ax.add_patch(rectangle)
            ax.text(x, y, node_text, fontsize=12, ha='center', va='center', zorder=3,
                    color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))
        else:
            pal.figura = FIGURA_RECTANGULO
            pal.tam_eje_y_figura = tam_figuras.RECTANGULO[1]
            pal.multiplicador_borde_figura = tam_figuras.RECTANGULO[0] * len(node_text)
            rectangle_width = tam_figuras.RECTANGULO[0] * 2 * len(node_text)
            height = 1  # pal.dimension_y
            tamano_texto = 12

            rectangle = Rectangle(
                xy=(x - rectangle_width / 2, y - height * 0.4),
                width=rectangle_width,
                height=height,
                color=dict_color_figura.get(pal.lugar_sintactico, colores.default),
                zorder=2)
            ax.add_patch(rectangle)
            ax.text(x, y, node_text, fontsize=12, ha='center', va='center',
                    zorder=3, color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))

            # ellipse_width = 0.1 * len(node) + 0.2
            # ellipse_height = 0.4
            # ellipse = Ellipse((x, y), width=ellipse_width, height=ellipse_height, color=dict_color_figura[None], zorder=2)
            # ax.add_patch(ellipse)
            # ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3, color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))
