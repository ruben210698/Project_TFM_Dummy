import math

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, RegularPolygon, Ellipse, Rectangle

from utils.Palabra import Palabra
from utils.Relacion import Relacion
from utils.Relacion import DIR_ABAJO, DIR_ARRIBA, DIR_DCHA, DIR_IZQ




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

PREDICADO = "predicado"
CCL = "CCL"
CCT = "CCT"
CD = "CD"
ATRIBUTO = "ATRIBUTO"
CCCOMP = "CCCOMP"
SUJETO = "sujeto"
NOMBRE = "nombre"
VERBO = "verbo"

max_axis_x = 0
min_axis_x = 0
max_axis_y = 0
min_axis_y = 0





# Función para dibujar aristas con flechas
def draw_edge(ax, u, v, width=1.0, color='k', label='', label_offset=(0, 0)):
    arrow = FancyArrowPatch(u, v, arrowstyle='->', mutation_scale=20, linewidth=width, color=color)
    ax.add_patch(arrow)
    if label:
        x_label = (u[0] + v[0]) / 2 + label_offset[0]
        y_label = (u[1] + v[1]) / 2 + label_offset[1]
        ax.text(x_label, y_label, label, fontsize=12, ha='center', va='center', zorder=3)

def get_importance_dict(list_palabras):
    new_dict = {}
    for pal in list_palabras:
        new_dict[pal] = {"importancia": pal.importancia, "dimension":pal.dimension}
    #ordenar el diccionario por importancia
    new_dict = dict(sorted(new_dict.items(), key=lambda item: item[1]["importancia"]))
    return new_dict


def get_next_direction(matrix_dim, x_ini, x_fin, y, rel):
    pos_x_media = (x_ini + x_fin) // 2
    # Saco el tamaño texto impar para las relaciones que vayan a abajo o arriba.
    # Ya que deben ocupar de ancho el tamaño del texto de forma simetrica
    tam_text_origen = rel.tam_texto if rel.tam_texto > 0 else 1
    tam_text_impar = tam_text_origen if tam_text_origen % 2 != 0 else tam_text_origen + 1
    # comprueba si el espacio inmediatamente a la derecha está libre
    if x_fin + 1 < len(matrix_dim[y]) and matrix_dim[y][x_fin + 1] == 0 and matrix_dim[y][x_fin + 2] == 0:
        return x_fin + 1 , y, DIR_DCHA, tam_text_origen

    # comprueba si el espacio inmediatamente abajo está libre
    if y + 2 < len(matrix_dim) and matrix_dim[y + 2][pos_x_media] == 0 * (len(matrix_dim[y]) - x_ini):
        return pos_x_media, y + 2, DIR_ABAJO, tam_text_impar

    # comprueba si el espacio inmediatamente arriba está libre
    if y - 2 >= 0 and matrix_dim[y - 2][pos_x_media] == 0 * (len(matrix_dim[y]) - x_ini):
        return pos_x_media, y - 2, DIR_ARRIBA, tam_text_impar

    # comprueba si el espacio inmediatamente a la izquierda está libre
    if x_ini - 1 >= 0 and x_ini - 1 >= 0 and matrix_dim[y][x_ini - 1] == 0:
        return x_ini - 1 , y, DIR_IZQ, tam_text_origen

    #######
    # TODO quitar esto
    #######
    if y - 4 >= 0 and matrix_dim[y - 4][pos_x_media] == 0 * (len(matrix_dim[y]) - x_ini):
        return pos_x_media, y - 4, DIR_ARRIBA, tam_text_impar
    if y - 6 >= 0 and matrix_dim[y - 6][pos_x_media] == 0 * (len(matrix_dim[y]) - x_ini):
        return pos_x_media, y - 6, DIR_ARRIBA, tam_text_impar
    if y - 8 >= 0 and matrix_dim[y - 8][pos_x_media] == 0 * (len(matrix_dim[y]) - x_ini):
        return pos_x_media, y - 8, DIR_ARRIBA, tam_text_impar

    return None, None, None


def reducir_tam_matriz(matrix_dim):
    imprimir_matriz(matrix_dim)
    # Reducir Matriz
    matrix_dim_copy = matrix_dim.copy()
    for x in matrix_dim_copy:
        if sum(x) == 0:
            matrix_dim.pop(0)
        else:
            break
    imprimir_matriz(matrix_dim)
    matrix_dim_reverse = matrix_dim.copy()
    matrix_dim_reverse.reverse()
    for x in matrix_dim_reverse:
        if sum(x) == 0:
            matrix_dim.pop()
        else:
            break
    imprimir_matriz(matrix_dim)
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


def imprimir_matriz(matriz):
    print("-----------------------------------------------------------------------")
    i, j = 0, 0
    print(f"    ", end="")
    for elemento in matriz[0]:
        print(f"{i:<4}", end="")
        i += 1
    print()

    for fila in matriz:
        print(f"{j:<4}", end="")
        for elemento in fila:
            if elemento == 0:
                print(f"{elemento:<4}", end="")
            else:
                print(f"{elemento:<4}", end="")
        j += 1
        print()
    print("-----------------------------------------------------------------------")



def get_suggested_position(matrix_dim, palabra):
    list_relaciones = Palabra.relaciones_dict_dest[palabra]

    y, x = get_most_centered_pos(matrix_dim)
    id_to_find = 0
    relacion = None
    # x_ini = -1
    # x_fin = -1
    # y_ini = -1
    # y_fin = -1
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
    rango = palabra.dimension + 1
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

    return y, x + rango//2, id_to_find


def get_most_centered_pos(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    center_row = rows // 2
    center_col = cols // 2
    min_distance = math.inf
    closest_zero = None

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 0:
                distance = math.sqrt((i - center_row) ** 2 + (j - center_col) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_zero = (i, j)

    return closest_zero

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


def get_position_dict(list_palabras):
    importance_dict = get_importance_dict(list_palabras)
    max_importance = max([value['importancia'] for key, value in importance_dict.items()])
    matrix_dim = [[] for i in range(15)]
    for y in range(15):
        matrix_dim[y] += [0 for x in range(70)]
    print(matrix_dim)
    pos_y_media = len(matrix_dim) // 2
    pos_x_media = len(matrix_dim[0]) // 2

    pos = {}
    dict_rel_direction = {}

    list_palabras_ordenadas = list(importance_dict.keys())
    while len(list_palabras_ordenadas) != 0:
        palabra = list_palabras_ordenadas.pop(0)

        pos_y_sugerida, pos_x_sugerida, id_to_find = get_suggested_position(matrix_dim, palabra)
        imprimir_matriz(matrix_dim)
        print(f"Matrix: {palabra.texto}")

        # obtener la posicion del primer 0 de la lista
        axis_y = pos_y_sugerida
        pos0 = pos_x_sugerida #+ matrix_dim[axis_y][pos_x_sugerida:].index(id_to_find)

        pos.update({palabra: (pos0 - palabra.dimension // 2 - pos_x_media , axis_y - pos_y_media)})

        # reemplazar los 0s por 1s para range(value['dimension']+2)
        matrix_dim[axis_y][pos0:pos0 + palabra.dimension + 2] = [palabra.id for x in range(palabra.dimension + 2)]

        palabra.has_been_plotted = True
        list_relaciones_pal = Palabra.relaciones_dict_origen.get(palabra)
        added_list_pal_dest = [rel.pal_dest for rel in list_relaciones_pal]
        list_palabras_ordenadas = insert_start_list(list_palabras_ordenadas, added_list_pal_dest)
        for relation in list_relaciones_pal:
            rel_x, rel_y, direction, ancho_flecha = get_next_direction(
                matrix_dim, pos0, pos0 + palabra.dimension + 1, axis_y, relation)
            relation.direction = direction
            dict_rel_direction.update({relation.id: direction})
            if direction == DIR_DCHA:
                for i in range(ancho_flecha+1):
                    matrix_dim[rel_y][rel_x + i] = relation.id
            elif direction == DIR_IZQ:
                for i in range(ancho_flecha+1):
                    matrix_dim[rel_y][rel_x - i] = relation.id
            else:
                matrix_dim[rel_y][rel_x] = relation.id
                for i in range(ancho_flecha):
                    matrix_dim[rel_y][rel_x - ancho_flecha//2 + i] = relation.id
            imprimir_matriz(matrix_dim)

    return pos, matrix_dim


def unir_relaciones(list_relaciones):
    # En caso de que 2 relaciones tengan el mismo origen y destino, unirlas
    list_relaciones = list(set(list_relaciones))
    list_relaciones_new = list_relaciones.copy()
    list_modified = []
    for rel in list_relaciones:
        for rel2 in list_relaciones:
            if rel2 not in list_modified and rel not in list_modified and \
                rel != rel2 and rel.pal_origen == rel2.pal_origen and rel.pal_dest == rel2.pal_dest:
                if rel.position_doc <= rel2.position_doc:
                    rel.texto = rel.texto + " " + rel2.texto
                else:
                    rel.texto = rel2.texto + " " + rel.texto
                    rel.position_doc = rel2.position_doc
                rel.importancia = min(rel.importancia, rel2.importancia)
                rel.tam_texto = rel.tam_texto + rel2.tam_texto
                list_relaciones_new.remove(rel2)
                list_modified.append(rel)
                rel2.delete_relation()

    return list_relaciones_new



def print_graph(texto, list_palabras, list_relaciones):
    list_relaciones = unir_relaciones(list_relaciones)

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
    for relation in list_relaciones:
        G.add_edge(relation.pal_origen, relation.pal_dest)

    # Crear posiciones de nodos
    position_elems, matrix_dim = get_position_dict(list_palabras)

    #Convertir el position elements sustituyendo el primero objeto por el texto
    position_elems_deprec = {}
    for pal in list_palabras:
        position_elems_deprec[pal.texto] = position_elems[pal]



    matrix_dim = reducir_tam_matriz(matrix_dim)

    imprimir_matriz(matrix_dim)
    pos_y_media = len(matrix_dim)//2
    pos_x_media = len(matrix_dim[0])//2
    max_axis_y = len(matrix_dim) - pos_y_media + 2
    min_axis_y = 0 - pos_y_media - 2
    max_axis_x = max([len(x) for x in matrix_dim]) + 3
    min_axis_x = -3

    fig, ax = plt.subplots(figsize=(12, 8))

    # Colores
    light_blue = "#4da6ff"
    green = "#33CC00"
    red = "#FF3333"
    purple = "#9933FF"

    dict_color = {
        SUJETO: light_blue,
        CD: red,
        CCL: purple,
        CCT: green,
        ATRIBUTO: light_blue,
        None: '#EEE000'
    }


    # Dibujar nodos
    for pal, (x, y) in position_elems.items():
        node = pal.texto
        if pal.lugar_sintactico == SUJETO:
            ellipse_width = 0.1 * len(node) + 0.2
            ellipse_height = 0.4
            ellipse = Ellipse((x, y), width=ellipse_width, height=ellipse_height, color=dict_color[SUJETO], zorder=2)
            ax.add_patch(ellipse)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)

        elif pal.lugar_sintactico == CD:
            rectangle_width = 0.1 * len(node) + 0.2
            rectangle = Rectangle((x - rectangle_width / 2, y - 0.25), width=rectangle_width, height=0.5, color=dict_color[CD], zorder=2)
            ax.add_patch(rectangle)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)

        elif pal.lugar_sintactico == CCL:
            polygon_radius = 0.06 * len(node) + 0.1
            polygon = RegularPolygon((x, y), numVertices=6, radius=polygon_radius, orientation=0, color=dict_color[CCL], zorder=2)
            ax.add_patch(polygon)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)

        elif pal.lugar_sintactico == CCT or pal.lugar_sintactico == ATRIBUTO:
            rectangle_width = 0.1 * len(node) + 0.2
            rectangle = Rectangle((x - rectangle_width / 2, y - 0.25), width=rectangle_width, height=0.5, color=dict_color[CCT],
                                  zorder=2)
            ax.add_patch(rectangle)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)
        else:
            ellipse_width = 0.1 * len(node) + 0.2
            ellipse_height = 0.4
            ellipse = Ellipse((x, y), width=ellipse_width, height=ellipse_height, color=dict_color[None], zorder=2)
            ax.add_patch(ellipse)
            ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)




    # Dibujar aristas
    for relation in list_relaciones:
        color = dict_color.get(relation.lugar_sintactico,dict_color[None])
        x_origen = 0
        x_dest = 0
        if relation.direction == DIR_DCHA:
            x_origen = position_elems_deprec[relation.pal_origen.texto][0] + relation.pal_origen.dimension//2
            x_dest = position_elems_deprec[relation.pal_dest.texto][0] - relation.pal_dest.dimension//2
        if relation.direction == DIR_IZQ:
            x_origen = position_elems_deprec[relation.pal_origen.texto][0] - relation.pal_origen.dimension//2
            x_dest = position_elems_deprec[relation.pal_dest.texto][0] + relation.pal_dest.dimension//2



        draw_edge(
            ax,
            (x_origen, position_elems_deprec[relation.pal_origen.texto][1]),
            (x_dest, position_elems_deprec[relation.pal_dest.texto][1]),
            color=color,
            label=relation.texto,
            label_offset=(0, 0.1)
        )

    #draw_edge(ax, position_elems_deprec["ruben"], position_elems_deprec["pescado"], color=light_blue, label='come', label_offset=(0, 0.1))
    #draw_edge(ax, position_elems_deprec["pescado"], position_elems_deprec["restaurante"], color=light_blue, label='en', label_offset=(0, 0.1))
    #draw_edge(ax, position_elems_deprec["restaurante"], position_elems_deprec["pepe"], color=green, label='de', label_offset=(0, 0.1))



    # Configurar límites y aspecto del gráfico
    ax.set_ylim(min_axis_y, max_axis_y)
    ax.set_xlim(min_axis_x, max_axis_x)
    ax.set_aspect('equal')
    ax.axis('on')

    plt.show()



texto = "Ruben cocina hamburguesas en la Freidora de aire"
list_palabras = []
list_relaciones = []

list_palabras.append(Palabra('Ruben', 'PROPN', 'ROOT', 1, 99, 0, False, 'Ruben', 0))
list_palabras.append(Palabra('hamburguesas', 'ADJ', 'amod', 2, 99, 0, False, 'hamburguesa', 13))
list_palabras.append(Palabra('Freidora', 'PROPN', 'nmod', 3, 99, 0, False, 'Freidora', 32))
list_palabras.append(Palabra('aire', 'PROPN', 'flat', 4, 99, 0, False, 'aire', 44))
list_relaciones.append(Relacion('cocina', Palabra.palabras_dict.get('Ruben'), Palabra.palabras_dict.get('hamburguesa'), 5, 'amod', -2, 197))
list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('Freidora'), 17, 'nmod', -3, 197))
list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('aire'), 17, 'flat', -4, 197))
list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('Freidora'), 20, 'nmod', -5, 197))
list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('aire'), 20, 'flat', -6, 197))
list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('Freidora'), Palabra.palabras_dict.get('aire'), 38, 'flat', -7, 197))

print_graph(texto, list_palabras, list_relaciones)


