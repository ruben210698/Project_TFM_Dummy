import math

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, RegularPolygon, Ellipse, Rectangle

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
from visualizacion.utils.matrix_functions import generate_matrix

LINEAS_SEP_FILA = 5

PRINT_MATRIX = False
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


def reducir_tam_matriz(matrix_dim):
    # Reducir Matriz
    matrix_dim = matrix_dim.copy()
    matrix_dim_copy = matrix_dim.copy()
    for x in matrix_dim_copy:
        if sum(x) == 0:
            matrix_dim.pop(0)
        else:
            break
    matrix_dim_reverse = matrix_dim.copy()
    matrix_dim_reverse.reverse()
    for x in matrix_dim_reverse:
        if sum(x) == 0:
            matrix_dim.pop()
        else:
            break
    matrix_dim_transpose = [list(fila) for fila in zip(*matrix_dim)]
    matrix_dim_transpose_copy = matrix_dim_transpose.copy()
    for x in matrix_dim_transpose_copy:
        if sum(x) == 0:
            matrix_dim_transpose.pop(0)
        else:
            break
    matrix_dim_transpose_reverse = matrix_dim_transpose.copy()
    matrix_dim_transpose_reverse.reverse()
    for x in matrix_dim_transpose_reverse:
        if sum(x) == 0:
            matrix_dim_transpose.pop()
        else:
            break
    matrix_dim = [list(fila) for fila in zip(*matrix_dim_transpose)]
    return matrix_dim


def imprimir_matriz(matriz, apply_num_inicial_col=True):
    try:
        if not PRINT_MATRIX:
            return
        matriz = matriz.copy()
        matriz = reducir_tam_matriz(matriz)
        print("-----------------------------------------------------------------------")
        i, j = 0, 0
        print(f"    ", end="")
        for elemento in matriz[0]:
            print(f"{i:<4}", end="")
            i += 1
        print()

        for fila in matriz:
            print(f"{j:<4}", end="")
            num_col = 0
            for elemento in fila:
                if elemento == 0:
                    print(f"{elemento:<4}", end="")
                else:
                    print(f"{elemento:<4}", end="")
                num_col += 1
            j += 1
            print()
        print("-----------------------------------------------------------------------")
    except Exception as e:
        print(e)
        pass


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




def update_palabras_in_matrix(matrix_dim, palabra, axis_y, axis_x):
    # bucle que recorre palabra.dimension_y desde -palabra.dimension_y//2 hasta palabra.dimension_y//2
    for y in range(palabra.dimension_y):
        axis_y_loop = axis_y + y - palabra.dimension_y // 2
        matrix_dim[axis_y_loop][axis_x:axis_x + palabra.dimension + palabra.cte_sum_x] = [palabra.id for x in
                                                                                          range(palabra.dimension + 2)]


def get_position_word_recursive(position_elems, matrix_dim, palabra, pos_y_media, pos_x_media, list_relaciones,
                                relation=None):
    list_palabras_representadas = []
    print(f"Matrix: {palabra.texto}")
    aaaaaaaaaaa = palabra.texto
    if palabra.texto == 'majestuosas y extensas':
        print("hola")

    axis_y, axis_x, matrix_dim = get_next_location(matrix_dim, palabra, relation)
    if axis_y is None or axis_x is None:
        return None, None, None
    palabra.pos_y = axis_y
    palabra.pos_x = axis_x
    position_elems.update({
        palabra: (
            axis_x - pos_x_media,
            axis_y - pos_y_media
        )})

    # reemplazar los 0s por IDs para range(value['dimension']+2)
    update_palabras_in_matrix(matrix_dim, palabra, axis_y, axis_x)

    imprimir_matriz(matrix_dim)
    palabra.has_been_plotted = True

    list_relaciones_pal = Palabra.relaciones_dict_origen.get(palabra, [])

    list_direcciones_orden = []
    if len(list_relaciones_pal) > 0:
        list_relaciones_pal.sort(
            key=lambda x: x.pal_dest.grafos_aproximados[0] if len(x.pal_dest.grafos_aproximados) > 0 else 0,
            reverse=True)
        find_dir = DICT_DIR_BY_ORIGEN.get(palabra.direccion_origen)
        # FIXME: meter aqui un try-except por si supera 7 elementos.
        list_direcciones_orden = find_dir[len(list_relaciones_pal) - 1]
        palabra.lista_direcciones_orden = list_direcciones_orden

    num_dir_orden = -1
    num_relacion = -1
    while num_dir_orden < len(list_direcciones_orden) - 1:
        num_dir_orden += 1
        num_relacion += 1
        relation = list_relaciones_pal[num_relacion]

        palabra.pos_actual_recorrer_dir_relaciones = num_dir_orden
        if relation.pal_dest.has_been_plotted:
            continue

        dir_actual = list_direcciones_orden[num_dir_orden]
        relation.direccion_actual = dir_actual
        relation.pal_dest.direccion_origen = dir_actual

        print_graph(list_palabras_representadas, list_relaciones, position_elems, matrix_dim)
        if palabra.texto == 'majestuosas y extensas':
            print("hola")

        list_palabras_representadas_new, position_elems_2, matrix_dim_2 = \
            get_position_word_recursive(position_elems, matrix_dim, relation.pal_dest, pos_y_media, pos_x_media,
                                        list_relaciones, relation)

        if list_palabras_representadas_new is None or position_elems is None or matrix_dim is None:
            print("No se ha podido representar el grafo")
            list_direcciones_orden = palabra.lista_direcciones_orden
            list_palabras_representadas_new = []
            num_relacion -= 1
        else:
            position_elems = position_elems_2
            matrix_dim = matrix_dim_2


        list_palabras_representadas += list_palabras_representadas_new

    list_palabras_representadas.append(palabra)

    return list_palabras_representadas, position_elems, matrix_dim


def get_position_dict(list_palabras, list_relaciones):
    importance_dict = get_importance_dict(list_palabras)
    matrix_dim, pos_y_media, pos_x_media = generate_matrix(list_palabras)

    position_elems = {}
    dict_rel_direction = {}

    list_palabras_ordenadas = list(importance_dict.keys())
    while len(list_palabras_ordenadas) != 0:
        palabra = list_palabras_ordenadas.pop(0)

        list_palabras_representadas, position_elems, matrix_dim = \
            get_position_word_recursive(position_elems, matrix_dim, palabra, pos_y_media, pos_x_media, list_relaciones)

        print_graph(list_palabras_representadas, list_relaciones, position_elems, matrix_dim)
        # quitar de list_palabras_ordenadas las palabras que ya han sido representadas
        list_palabras_ordenadas = [pal for pal in list_palabras_ordenadas if pal not in list_palabras_representadas]
        list_palabras_ordenadas.sort(key=lambda x: x.grafos_aproximados[0] if len(x.grafos_aproximados) > 0 else 0,
                                     reverse=True)

        print_graph(list_palabras, list_relaciones, position_elems, matrix_dim)

    position_elems = reducir_posiciones_finales_eje_y(position_elems)

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


def print_graph(list_palabras, list_relaciones, position_elems, matrix_dim, final=False):
    if PRINT_GRAPH or final:
        _print_graph(list_palabras, list_relaciones, position_elems, matrix_dim)

def _print_graph(list_palabras, list_relaciones, position_elems, matrix_dim):
    position_elems_deprec = {}
    for pal in list_palabras:
        try:
            position_elems_deprec[pal.texto] = position_elems[pal]
        except Exception as _:
            pass

    imprimir_matriz(matrix_dim, apply_num_inicial_col=False)
    matrix_dim_reduced = matrix_dim.copy()
    matrix_dim_reduced = reducir_tam_matriz(matrix_dim_reduced)

    imprimir_matriz(matrix_dim_reduced, apply_num_inicial_col=False)

    max_axis_y = max([x[1] for x in position_elems.values()]) + 3
    min_axis_y = min([x[1] for x in position_elems.values()]) - 3
    max_axis_x = max([x[0] for x in position_elems.values()]) + 5
    min_axis_x = min([x[0] for x in position_elems.values()]) - 5

    dif_y = abs(max_axis_y - min_axis_y)//2
    dif_x = abs(max_axis_x - min_axis_x)//2

    fig, ax = plt.subplots(figsize=(dif_x, dif_y))
    #fig, ax = plt.subplots(figsize=(24, 16))
    #fig, ax = plt.subplots()

    # Dibujar nodos
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
            height = 1 #pal.dimension_y
            tamano_texto = 12

            rectangle = Rectangle(
                xy=(x - rectangle_width / 2, y - height * 0.4),
                width=rectangle_width,
                height=height,
                color=dict_color_figura.get(pal.lugar_sintactico, colores.default),
                zorder=2)
            ax.add_patch(rectangle)
            ax.text(x, y, node_text, fontsize=12, ha='center', va='center',
                    zorder=3,  color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))


            # ellipse_width = 0.1 * len(node) + 0.2
            # ellipse_height = 0.4
            # ellipse = Ellipse((x, y), width=ellipse_width, height=ellipse_height, color=dict_color_figura[None], zorder=2)
            # ax.add_patch(ellipse)
            # ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3, color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))



    # Dibujar aristas
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
            x_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][0]
            x_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][0]
            y_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][1]
            y_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][1]
            if relation_draw.direccion_actual == DIR_DCHA:
                x_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][
                                    0] + relation_draw.pal_origen.multiplicador_borde_figura - 0.25
                x_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][
                                  0] - relation_draw.pal_dest.multiplicador_borde_figura
            elif relation_draw.direccion_actual == DIR_IZQ:
                x_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][
                                    0] - relation_draw.pal_origen.dimension // 2
                x_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][
                                  0] + relation_draw.pal_dest.dimension // 2
            elif relation_draw.direccion_actual == DIR_ARRIBA:
                y_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][1]
                y_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][
                                  1] - relation_draw.pal_dest.tam_eje_y_figura
                x_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][
                                  0] - relation_draw.pal_dest.multiplicador_borde_figura
            elif relation_draw.direccion_actual == DIR_ABAJO:
                y_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][1]
                y_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][
                                  1] + relation_draw.pal_dest.tam_eje_y_figura
                x_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][
                                  0] + relation_draw.pal_dest.multiplicador_borde_figura
            else:
                # TODO me faltan las de los 45º
                x_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][
                                    0] + relation_draw.pal_origen.multiplicador_borde_figura - 0.25
                x_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][
                                  0] - relation_draw.pal_dest.multiplicador_borde_figura - 0.25

            draw_edge(
                ax,
                (x_origen_draw, y_origen_draw),
                (x_dest_draw, y_dest_draw),
                color=color,
                label=relation_draw.texto,
                label_offset=(0, 0.4)
            )
        except Exception as e:
            pass

    # draw_edge(ax, position_elems_deprec["ruben"], position_elems_deprec["pescado"], color=light_blue, label='come', label_offset=(0, 0.1))
    # draw_edge(ax, position_elems_deprec["pescado"], position_elems_deprec["restaurante"], color=light_blue, label='en', label_offset=(0, 0.1))
    # draw_edge(ax, position_elems_deprec["restaurante"], position_elems_deprec["pepe"], color=green, label='de', label_offset=(0, 0.1))

    # Configurar límites y aspecto del gráfico
    ax.set_ylim(min_axis_y, max_axis_y)
    ax.set_xlim(min_axis_x, max_axis_x)
    ax.set_aspect('equal')
    ax.axis('on')

    plt.show()
