import math

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, RegularPolygon, Ellipse, Rectangle

from utils.Palabra import Palabra
from utils.Relacion import Relacion
from utils.Relacion import DIR_ABAJO, DIR_ARRIBA, DIR_DCHA, DIR_IZQ

from constants.figuras import *
from constants.type_morfologico import *
from constants.type_sintax import *
from constants import type_sintax
from constants import colores_figura, colores_figura_letra, colores
from constants.figuras import *
from constants import tam_figuras
from utils.utils_text import unir_list_all_relaciones, unir_siglos_annos_all_list

LINEAS_SEP_FILA = 5
DIM_Y_MATRIX = 15
DIM_X_MATRIX = 100
DIM_Y_MATRIX = 500
DIM_X_MATRIX = 20000
PRINT_MATRIX = False

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

#TODO:
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
        new_dict[pal] = {"importancia": pal.importancia, "dimension":pal.dimension}
    #ordenar el diccionario por importancia
    new_dict = dict(sorted(new_dict.items(), key=lambda item: item[1]["importancia"]))
    return new_dict

def get_direction_by_pal_plotted(matrix_dim, rel, x_ini, y_ini):
    if rel.pal_dest.pos_x is None:
        return None, None, None, None

    tam_text_origen = rel.tam_texto if rel.tam_texto > 0 else 1
    tam_text_impar = tam_text_origen if tam_text_origen % 2 != 0 else tam_text_origen + 1

    x_fin = rel.pal_dest.pos_x
    y_fin = rel.pal_dest.pos_y
    if y_ini == y_fin and x_ini < x_fin:
        return x_ini, y_fin, DIR_DCHA, tam_text_origen
    elif y_ini == y_fin and x_ini > x_fin:
        return x_fin, y_fin, DIR_IZQ, tam_text_origen
    elif y_ini > y_fin:
        return x_fin, y_ini, DIR_ABAJO, tam_text_impar
    elif y_ini < y_fin:
        return x_fin, y_fin, DIR_ARRIBA, tam_text_impar

    return None, None, None, None

def get_next_direction(matrix_dim, x_ini, x_fin, y, rel):
    pos_x_media = (x_ini + x_fin) // 2
    # Saco el tamaño texto impar para las relaciones que vayan a abajo o arriba.
    # Ya que deben ocupar de ancho el tamaño del texto de forma simetrica
    tam_text_origen = rel.tam_texto if rel.tam_texto > 0 else 1
    tam_text_impar = tam_text_origen if tam_text_origen % 2 != 0 else tam_text_origen + 1

    # comprueba si el espacio inmediatamente a la derecha está libre
    if x_fin + 1 < len(matrix_dim[y]) and matrix_dim[y][x_fin + 1] == 0 and matrix_dim[y][x_fin + 2] == 0:
        return x_fin + 1, y, DIR_DCHA, tam_text_origen

    # comprueba si el espacio inmediatamente abajo está libre
    if y + LINEAS_SEP_FILA < len(matrix_dim) and matrix_dim[y + LINEAS_SEP_FILA][pos_x_media] == 0 * (len(matrix_dim[y]) - x_ini):
        return pos_x_media, y + LINEAS_SEP_FILA, DIR_ABAJO, tam_text_impar

    # comprueba si el espacio inmediatamente arriba está libre
    if y - LINEAS_SEP_FILA >= 0 and matrix_dim[y - LINEAS_SEP_FILA][pos_x_media] == 0 * (len(matrix_dim[y]) - x_ini):
        return pos_x_media, y - LINEAS_SEP_FILA, DIR_ARRIBA, tam_text_impar

    # comprueba si el espacio inmediatamente a la izquierda está libre
    if x_ini - 1 >= 0 and x_ini - 1 >= 0 and matrix_dim[y][x_ini - 1] == 0:
        return x_ini - 1 , y, DIR_IZQ, tam_text_origen

    #######
    # TODO quitar esto
    #######
    if y - 4 >= 0 and matrix_dim[y - 4][pos_x_media] == 0:
        return pos_x_media, y - 4, DIR_ARRIBA, tam_text_impar
    if y - 6 >= 0 and matrix_dim[y - 6][pos_x_media] == 0:
        return pos_x_media, y - 6, DIR_ARRIBA, tam_text_impar
    if y - 8 >= 0 and matrix_dim[y - 8][pos_x_media] == 0:
        return pos_x_media, y - 8, DIR_ARRIBA, tam_text_impar
    if y - 8 >= 0 and matrix_dim[y - 10][pos_x_media] == 0:
        return pos_x_media, y - 8, DIR_ARRIBA, tam_text_impar
    if y - 8 >= 0 and matrix_dim[y - 12][pos_x_media] == 0:
        return pos_x_media, y - 8, DIR_ARRIBA, tam_text_impar
    if y - 8 >= 0 and matrix_dim[y - 14][pos_x_media] == 0:
        return pos_x_media, y - 8, DIR_ARRIBA, tam_text_impar
    if y - 8 >= 0 and matrix_dim[y - 16][pos_x_media] == 0:
        return pos_x_media, y - 8, DIR_ARRIBA, tam_text_impar
    if y - 8 >= 0 and matrix_dim[y - 18][pos_x_media] == 0:
        return pos_x_media, y - 8, DIR_ARRIBA, tam_text_impar
    if y - 8 >= 0 and matrix_dim[y - 20][pos_x_media] == 0:
        return pos_x_media, y - 8, DIR_ARRIBA, tam_text_impar

    return None, None, None


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


def imprimir_matriz(matriz, apply_num_inicial_col = True):
    if not PRINT_MATRIX:
        return
    print("-----------------------------------------------------------------------")
    if apply_num_inicial_col:
        NUM_INICIAL_COL = 50
    else:
        NUM_INICIAL_COL = 0

    i, j = 0, 0
    print(f"    ", end="")
    for elemento in matriz[0]:
        if i > NUM_INICIAL_COL:
            print(f"{i:<4}", end="")
        i += 1
    print()

    for fila in matriz:
        print(f"{j:<4}", end="")
        num_col = 0
        for elemento in fila:
            if num_col > NUM_INICIAL_COL:
                if elemento == 0:
                    print(f"{elemento:<4}", end="")
                else:
                    print(f"{elemento:<4}", end="")
            num_col += 1
        j += 1
        print()
    print("-----------------------------------------------------------------------")


def get_y_matrix(matrix, id):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == id:
                return i
    return None


def get_pal_suggested_position(matrix_dim, palabra):
    list_relaciones = Palabra.relaciones_dict_destino[palabra]

    y, x = get_most_centered_pos(matrix_dim)
    id_to_find = 0
    relacion = None
    # x_ini = -1
    # x_fin = -1
    # y_ini = -1
    # y_fin = -1
    if palabra.pos_x is not None and palabra.pos_y is not None:
        y = palabra.pos_y
        x = palabra.pos_x
    else:
        for rel in list_relaciones:
            for i in range(len(matrix_dim)):
                for j in range(len(matrix_dim[i])):
                    if matrix_dim[i][j] == rel.id:
                        y = i
                        x = j
                        #y_ini = i if y_ini == -1 else y_ini
                        #y_fin = i
                        #x_ini = j if x_ini == -1 else x_ini
                        #x_fin = j
                        id_to_find = rel.id
                        relacion = rel
                        break

        if relacion is not None and relacion.direction == DIR_DCHA:
            x = x + (relacion.tam_texto if relacion.tam_texto > 0 else 1)
        if relacion is not None and relacion.direction == DIR_IZQ:
            x = x - (relacion.tam_texto if relacion.tam_texto > 0 else 1)
    # cabe????
    rango = palabra.dimension + 4
    if relacion is not None and relacion.direction == DIR_IZQ:
        rango = -rango
    for x_test in range(rango):
        if matrix_dim[y][x_test + x] != id_to_find and matrix_dim[y][x_test + x] != 0:
            imprimir_matriz(matrix_dim)
            matrix_dim[y][x] = 0
            x = x - palabra.dimension // 2 - 1
            matrix_dim[y][x] = id_to_find
            imprimir_matriz(matrix_dim)
            break
    # TODO: ya se completará esto para que suba otra fila o para que haga cosas más complicadas
    if palabra.pos_x is None:
        return y, x + rango//2, id_to_find
    else:
        return y, x, id_to_find


def get_most_centered_pos(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    center_row = rows // 2
    center_col = cols // 2
    max_distance = max(center_row, center_col) + 1

    for distance in range(max_distance):
        for i in range(center_row - distance, center_row + distance + 1):
            j_left = center_col - distance
            j_right = center_col + distance

            # Comprobar si las posiciones están dentro de la matriz
            if i >= 0 and i < rows:
                if j_left >= 0 and j_left < cols and matrix[i][j_left] == 0:
                    return (i, j_left)
                if j_right >= 0 and j_right < cols and matrix[i][j_right] == 0:
                    return (i, j_right)

    return None

def insert_start_list(original_list, added_list):
    added_list.reverse()
    for pal in added_list:
        try:
            if pal in added_list:
                original_list.remove(pal)
                original_list.insert(0, pal)
        except Exception as e:
            pass

    return original_list


def get_position_dict(list_palabras, list_relaciones):
    importance_dict = get_importance_dict(list_palabras)
    max_importance = max([value['importancia'] for key, value in importance_dict.items()])
    matrix_dim = [[] for i in range(DIM_Y_MATRIX)]
    for y in range(DIM_Y_MATRIX):
        matrix_dim[y] += [0 for x in range(DIM_X_MATRIX)]
    #print(matrix_dim)
    pos_y_media = len(matrix_dim) // 2
    pos_x_media = len(matrix_dim[0]) // 2

    position_elems = {}
    dict_rel_direction = {}

    list_palabras_ordenadas = list(importance_dict.keys())
    while len(list_palabras_ordenadas) != 0:
        palabra = list_palabras_ordenadas.pop(0)

        pos_y_sugerida, pos_x_sugerida, id_to_find = get_pal_suggested_position(matrix_dim, palabra)
        imprimir_matriz(matrix_dim)
        print(f"Matrix: {palabra.texto}")

        # obtener la posicion del primer 0 de la lista
        axis_y = pos_y_sugerida
        pos0 = pos_x_sugerida #+ matrix_dim[axis_y][pos_x_sugerida:].index(id_to_find)

        position_elems.update({palabra: (pos0 - palabra.dimension // 2 - pos_x_media, axis_y - pos_y_media)})

        # reemplazar los 0s por 1s para range(value['dimension']+2)
        matrix_dim[axis_y][pos0:pos0 + palabra.dimension + 2] = [palabra.id for x in range(palabra.dimension + 2)]

        palabra.has_been_plotted = True
        list_relaciones_pal = Palabra.relaciones_dict_origen.get(palabra)
        added_list_pal_dest = [rel.pal_dest for rel in list_relaciones_pal]
        list_palabras_ordenadas = insert_start_list(list_palabras_ordenadas, added_list_pal_dest)
        for relation in list_relaciones_pal:
            if relation.pal_dest.pos_x is None:
                rel_x, rel_y, direction, ancho_flecha = get_next_direction(
                    matrix_dim, pos0, pos0 + palabra.dimension + 1, axis_y, relation)
            else:
                rel_x, rel_y, direction, ancho_flecha = get_direction_by_pal_plotted(matrix_dim, relation, pos0, axis_y)

            relation.direction = direction
            dict_rel_direction.update({relation.id: direction})
            if not relation.pal_dest.has_been_plotted and direction == DIR_DCHA:
                for i in range(ancho_flecha + ancho_flecha // 2):
                    matrix_dim[rel_y][rel_x + i] = relation.id
            elif not relation.pal_dest.has_been_plotted and direction == DIR_IZQ:
                for i in range(ancho_flecha + 1):
                    matrix_dim[rel_y][rel_x - i] = relation.id
            elif not relation.pal_dest.has_been_plotted:
                matrix_dim[rel_y][rel_x] = relation.id
                for i in range(ancho_flecha):
                    matrix_dim[rel_y][rel_x - ancho_flecha // 2 + i] = relation.id

            if not relation.pal_dest.has_been_plotted:
                pal_y, pal_x, _ = get_pal_suggested_position(matrix_dim, relation.pal_dest)
                relation.pal_dest.pos_x = pal_x
                relation.pal_dest.pos_y = pal_y
            imprimir_matriz(matrix_dim)
        print_graph(list_palabras, list_relaciones, position_elems, matrix_dim)

    return position_elems, matrix_dim




def generate_graph(texto, list_palabras, list_relaciones):
    list_relaciones = unir_list_all_relaciones(list_relaciones)
    list_palabras, list_relaciones = unir_siglos_annos_all_list(list_palabras, list_relaciones)
    list_relaciones = unir_list_all_relaciones(list_relaciones)

    dict_palabras = {}
    for palabra in list_palabras:
        dict_palabras[palabra.id] = palabra

    palabras_dict = Palabra.palabras_dict

    dic_relaciones = {}
    for r in list_relaciones:
        dic_relaciones[r.id] = r

    # Crear un grafo dirigido
    G = nx.DiGraph()

    # Añadir nodos y aristas
    list_relaciones_to_remove = []
    for relation in list_relaciones:
        if relation.pal_origen is None or relation.pal_dest is None:
            list_relaciones_to_remove.append(relation)
        else:
            G.add_edge(relation.pal_origen, relation.pal_dest)

    for relation in list_relaciones_to_remove:
        list_relaciones.remove(relation)
        relation.delete_relation()

    # Crear posiciones de nodos
    position_elems, matrix_dim = get_position_dict(list_palabras, list_relaciones)

    print_graph(list_palabras, list_relaciones, position_elems, matrix_dim)

def print_graph(list_palabras, list_relaciones, position_elems, matrix_dim):

    #Convertir el position elements sustituyendo el primero objeto por el texto
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


    fig, ax = plt.subplots(figsize=(12, 8))

    # Dibujar nodos
    for pal, (x, y) in position_elems.items():
        node = pal.texto
        if pal.lugar_sintactico.lower() in (TYPE_SINTAX_ROOT):
            pal.figura = FIGURA_ELIPSE
            pal.tam_eje_y_figura = tam_figuras.ELIPSE[1]
            pal.multiplicador_borde_figura = tam_figuras.ELIPSE[0] * len(node)
            ellipse_width = 0.6 * len(node)
            ellipse = Ellipse((x, y), width=ellipse_width, height=1, color=dict_color_figura.get(pal.lugar_sintactico, colores.default), zorder=2)
            ax.add_patch(ellipse)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3, color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))

        elif pal.lugar_sintactico.lower() in (TYPE_SINTAX_AMOD, TYPE_SINTAX_NMOD):
            pal.figura = FIGURA_RECTANGULO
            pal.tam_eje_y_figura = tam_figuras.RECTANGULO[1]
            pal.multiplicador_borde_figura = tam_figuras.RECTANGULO[0] * len(node)
            rectangle_width = 0.6 * len(node)
            rectangle = Rectangle((x - rectangle_width / 2, y - 0.4), width=rectangle_width, height=1, color=dict_color_figura.get(pal.lugar_sintactico, colores.default), zorder=2)
            ax.add_patch(rectangle)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3, color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))
#
        elif pal.lugar_sintactico.lower() in (TYPE_SINTAX_FLAT):
            pal.figura = FIGURA_HEXAGONO
            pal.tam_eje_y_figura = tam_figuras.HEXAGONO[1] * len(node)
            pal.multiplicador_borde_figura = tam_figuras.HEXAGONO[0] * len(node)
            polygon_radius = 0.4 * len(node)
            polygon = RegularPolygon((x, y), numVertices=6, radius=polygon_radius, orientation=0, color=dict_color_figura.get(pal.lugar_sintactico, colores.default), zorder=2)
            ax.add_patch(polygon)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3, color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))
#
        elif pal.lugar_sintactico.lower() in ():
            #TODO
            rectangle_width = 0.1 * len(node) + 0.2
            rectangle = Rectangle((x - rectangle_width / 2, y - 0.25), width=rectangle_width, height=0.5, color=dict_color_figura.get(pal.lugar_sintactico, colores.default),
                                  zorder=2)
            ax.add_patch(rectangle)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3, color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))
        else:
            ellipse_width = 0.1 * len(node) + 0.2
            ellipse_height = 0.4
            ellipse = Ellipse((x, y), width=ellipse_width, height=ellipse_height, color=dict_color_figura[None], zorder=2)
            ax.add_patch(ellipse)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3, color=dict_color_figura_letra.get(pal.lugar_sintactico, colores.black))





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
            if relation_draw.direction == DIR_DCHA:
                x_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][0] + relation_draw.pal_origen.multiplicador_borde_figura - 0.25
                x_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][0] - relation_draw.pal_dest.multiplicador_borde_figura
            elif relation_draw.direction == DIR_IZQ:
                x_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][0] - relation_draw.pal_origen.dimension//2
                x_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][0] + relation_draw.pal_dest.dimension//2
            elif relation_draw.direction == DIR_ARRIBA:
                y_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][1]
                y_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][1] - relation_draw.pal_dest.multiplicador_borde_figura
                x_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][0] - relation_draw.pal_dest.multiplicador_borde_figura
            elif relation_draw.direction == DIR_ABAJO:
                y_origen_draw = position_elems_deprec[relation_draw.pal_origen.texto][1]
                y_dest_draw = position_elems_deprec[relation_draw.pal_dest.texto][1]

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

    #draw_edge(ax, position_elems_deprec["ruben"], position_elems_deprec["pescado"], color=light_blue, label='come', label_offset=(0, 0.1))
    #draw_edge(ax, position_elems_deprec["pescado"], position_elems_deprec["restaurante"], color=light_blue, label='en', label_offset=(0, 0.1))
    #draw_edge(ax, position_elems_deprec["restaurante"], position_elems_deprec["pepe"], color=green, label='de', label_offset=(0, 0.1))



    # Configurar límites y aspecto del gráfico
    ax.set_ylim(min_axis_y, max_axis_y)
    ax.set_xlim(min_axis_x, max_axis_x)
    ax.set_aspect('equal')
    ax.axis('on')

    plt.show()



