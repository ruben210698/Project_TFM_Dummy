import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, RegularPolygon, Ellipse, Rectangle
import requests
from PIL import Image
import io

from visualizacion.Palabra import Palabra
from visualizacion.Relacion import Relacion
from visualizacion.Relacion import DIR_ABAJO, DIR_ARRIBA, DIR_DCHA, DIR_IZQ




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
- Que acepte relaciones a la izquierda (es decir, que la matriz empiece en la mitad y no en 0
- Que acepte más de 4 relaciones. Es decir, que para abajo me deje poner una de longitud 4 y otra en diagonal de lng 2 :) Y asi acepta 8.

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

texto3 = "ruben dibuja koalas en bañador saltando entre acantilados mientras su amigo graba la escena y se rie."

list_palabras = []
list_palabras.append(Palabra("ruben", NOMBRE, SUJETO, importancia=1))
list_palabras.append(Palabra("koalas", NOMBRE, CD, importancia=1))
list_palabras.append(Palabra("bañador", NOMBRE, CCL, importancia=2))
list_palabras.append(Palabra("acantilados", NOMBRE, CCL, importancia=2))
list_palabras.append(Palabra("amigo", NOMBRE, CCCOMP, importancia=3))
list_palabras.append(Palabra("escena", NOMBRE, CD, importancia=3))
list_palabras.append(Palabra("rie", VERBO, PREDICADO, importancia=3))

dict_palabras = {}
for palabra in list_palabras:
    dict_palabras[palabra.id] = palabra

palabras_dict = Palabra.palabras_dict

list_relaciones = []
list_relaciones.append(Relacion("dibuja", pal_origen=palabras_dict["ruben"], pal_dest=palabras_dict["koalas"], lugar_sintactico=PREDICADO, importancia=1))
list_relaciones.append(Relacion("en", pal_origen=palabras_dict["ruben"], pal_dest=palabras_dict["bañador"], lugar_sintactico=CCL, importancia=2))
list_relaciones.append(Relacion("saltando", pal_origen=palabras_dict["ruben"], pal_dest=palabras_dict["acantilados"], lugar_sintactico=CCL, importancia=2))
list_relaciones.append(Relacion("mientras", pal_origen=palabras_dict["ruben"], pal_dest=palabras_dict["amigo"], lugar_sintactico=CCCOMP, importancia=3))
list_relaciones.append(Relacion("graba", pal_origen=palabras_dict["amigo"], pal_dest=palabras_dict["escena"], lugar_sintactico=CD, importancia=3))
list_relaciones.append(Relacion("se rie", pal_origen=palabras_dict["amigo"], pal_dest=palabras_dict["escena"], lugar_sintactico=PREDICADO, importancia=3))

dic_relaciones = {}
for r in list_relaciones:
    dic_relaciones[r.id] = r



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


def get_next_direction(matrix_dim, x_ini, x_fin, y):
    pos_x_media = (x_ini + x_fin) // 2
    # comprueba si el espacio inmediatamente a la derecha está libre
    if x_fin + 1 < len(matrix_dim[y]) and matrix_dim[y][x_fin + 1] == 0:
        return x_fin + 1, y, DIR_DCHA

    # comprueba si el espacio inmediatamente abajo está libre
    if y + 2 < len(matrix_dim) and matrix_dim[y + 2][pos_x_media] == 0 * (len(matrix_dim[y]) - x_ini):
        return pos_x_media, y + 2, DIR_ABAJO

    # comprueba si el espacio inmediatamente arriba está libre
    if y - 2 >= 0 and matrix_dim[y - 2][pos_x_media] == 0 * (len(matrix_dim[y]) - x_ini):
        return pos_x_media, y - 2, DIR_ARRIBA

    # comprueba si el espacio inmediatamente a la izquierda está libre
    if x_ini - 1 >= 0 and x_ini - 1 >= 0 and matrix_dim[y][x_ini - 1] == 0:
        return x_ini - 1, y, DIR_IZQ

    return None, None


def imprimir_matriz(matriz):
    print("-----------------------------------------------------------------------")
    for fila in matriz:
        for elemento in fila:
            if elemento == 0:
                print(f"{elemento:<4}", end="")
            else:
                print(f"{elemento:<4}", end="")
        print()
    print("-----------------------------------------------------------------------")



def get_position_dict(list_palabras):
    importance_dict = get_importance_dict(list_palabras)
    # cojo el importance_dict y genero un diccionario con las posiciones
    # para cada palabra. De forma que quede una distancia de 2 entre palabras
    # y que las palabras más importantes estén en el centro
    # y las menos importantes en los extremos
    # y que tenga en cuenta tanto el eje x como el y

    # De momento se va a hacer simple: en el eje y, las palabras y en el eje x, la importancia.
    # La importancia 1, en el x=0, la 2, en el x=-2, la 3, en el x=2, etc.

    # obtener el valor maximo de importancia en importance_dict
    max_importance = max([value['importancia'] for key, value in importance_dict.items()])

    # Crear una lista con max_importance elementos
    # X2 ya que hay que dejar una diferencia de 2 entre palabras
    matrix_dim = [ [] for i in range(max_importance*2) ]
    pos_y_media = len(matrix_dim)//2

    for (palabra, value_import) in importance_dict.items():
        if value_import['importancia'] % 2 != 0:
            axis_y = pos_y_media + (value_import['importancia'] - 1)
            matrix_dim[axis_y] += [0 for x in range(value_import['dimension']+2)]
        else:
            axis_y = pos_y_media - value_import['importancia']
            matrix_dim[axis_y] += [0 for x in range(value_import['dimension']+2)]

    matrix_dim = [[] for i in range(15)]
    for y in range(15):
        matrix_dim[y] += [0 for x in range(50)]
    pos_y_media = len(matrix_dim) // 2
    pos_x_media = len(matrix_dim[0]) // 2
    print(matrix_dim)

    """
    Ahora tenemos una matriz bonita:
    [[], 
    [0, 0, 0, 0, 0], 
    [], 
    [0, 0, 0, 0, 0, 0, 0], 
    [], 
    [0, 0, 0]]
    Y vamos a ir rellenandola con 1s, por cada palabra que vayamos metiendo
    """
    pos = {}

    for (palabra, value_import) in importance_dict.items():

        print(f"Matrix: {palabra.texto}")
        if value_import['importancia'] % 2 != 0:
            axis_y = pos_y_media + (value_import['importancia'] - 1)
            # obtener la posicion del primer 0 de la lista
            pos0 = pos_x_media + matrix_dim[axis_y][pos_x_media:].index(0)
            pos.update({palabra: (value_import['dimension']//2 + pos0, axis_y - pos_y_media)})

            # reemplazar los 0s por 1s para range(value['dimension']+2)
            matrix_dim[axis_y][pos0:pos0+value_import['dimension']+2] = [palabra.id for x in range(value_import['dimension']+2)]
        else:
            axis_y = pos_y_media - value_import['importancia']
            # obtener la posicion del primer 0 de la lista
            pos0 = pos_x_media + matrix_dim[axis_y][pos_x_media:].index(0)
            pos.update({palabra: (value_import['dimension']//2 + pos0, axis_y - pos_y_media)})

            # reemplazar los 0s por 1s para range(value['dimension']+2)
            matrix_dim[axis_y][pos0:pos0 + value_import['dimension'] + 2] = [1 for x in range(value_import['dimension'] + 2)]

        palabra.has_been_plotted = True
        list_relaciones_pal = Palabra.relaciones_dict_origen.get(palabra)
        for relation in list_relaciones_pal:
            rel_x, rel_y, direction = get_next_direction(matrix_dim, pos0, pos0 + value_import['dimension'] + 1, axis_y)
            relation.direction = direction
            if rel_y == axis_y:
                matrix_dim[rel_y][rel_x] = relation.id
            else:
                matrix_dim[rel_y][rel_x] = relation.id
            imprimir_matriz(matrix_dim)

    return pos, matrix_dim

# Crear un grafo dirigido
G = nx.DiGraph()

# Añadir nodos y aristas
for relation in list_relaciones:
    G.add_edge(relation.pal_origen, relation.pal_dest)
# G.add_edge("Ruben", "pescado")
# G.add_edge("pescado", "en restaurante")
# G.add_edge("en restaurante", "Pepe")
# G.add_edge("Ruben", "Universidad Politécnica de Madrid")

# Crear posiciones de nodos
position_elems, matrix_dim = get_position_dict(list_palabras)

#Convertir el position elements sustituyendo el primero objeto por el texto
position_elems_deprec = {}
for pal in list_palabras:
    position_elems_deprec[pal.texto] = position_elems[pal]
# FIXME: eliminar


pos_media = len(matrix_dim)//2
max_axis_y = len(matrix_dim) - pos_media + 1
min_axis_y = 0 - pos_media - 1
max_axis_x = max([len(x) for x in matrix_dim]) + 1
min_axis_x = -1

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
    draw_edge(ax, position_elems_deprec[relation.pal_origen], position_elems_deprec[relation.pal_dest], color=color, label=relation.texto, label_offset=(0, 0.1))

#draw_edge(ax, position_elems_deprec["ruben"], position_elems_deprec["pescado"], color=light_blue, label='come', label_offset=(0, 0.1))
#draw_edge(ax, position_elems_deprec["pescado"], position_elems_deprec["restaurante"], color=light_blue, label='en', label_offset=(0, 0.1))
#draw_edge(ax, position_elems_deprec["restaurante"], position_elems_deprec["pepe"], color=green, label='de', label_offset=(0, 0.1))



# Configurar límites y aspecto del gráfico
ax.set_ylim(min_axis_y, max_axis_y)
ax.set_xlim(min_axis_x, max_axis_x)
ax.set_aspect('equal')
ax.axis('on')

plt.show()
