import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, RegularPolygon, Ellipse, Rectangle

from utils.Palabra import Palabra
from utils.Relacion import Relacion

PREDICADO = "predicado"
CCL = "CCL"
CCT = "CCT"
CD = "CD"
SUJETO = "sujeto"
NOMBRE = "nombre"
VERBO = "verbo"

max_axis_x = 0
min_axis_x = 0
max_axis_y = 0
min_axis_y = 0

texto1 = "Rubén come pescado en restaurante de Pepe al mediodia"
list_palabras = []
#     def __init__(self, tesssssxto, tipo, lugar_sintactico, id=None, importancia=1):
list_palabras.append(Palabra("Ruben", NOMBRE, SUJETO, importancia=1))
#list_palabras.append(Palabra("come", "verbo", "predicado", importancia=1))
list_palabras.append(Palabra("pescado", NOMBRE, CD, importancia=1))
#list_palabras.append(Palabra("en", "determinante", CCL, importancia=2))
list_palabras.append(Palabra("restaurante", NOMBRE, CCL, importancia=2))
list_palabras.append(Palabra("Pepe", NOMBRE, CCL, importancia=2))
list_palabras.append(Palabra("mediodia", NOMBRE, CCT, importancia=3))

list_relaciones = []
list_relaciones.append(Relacion("come", pal_origen="ruben", pal_dest="pescado", lugar_sintactico=PREDICADO, importancia=1))
list_relaciones.append(Relacion("en", pal_origen="pescado", pal_dest="restaurante", lugar_sintactico=CCL, importancia=2)) #Aquí qué seria, supongo que el sujeto entero, pero cómo lo pongo :(
list_relaciones.append(Relacion("de", pal_origen="restaurante", pal_dest="pepe", lugar_sintactico=CCL, importancia=2))
list_relaciones.append(Relacion("al", pal_origen="pescado", pal_dest="mediodia", lugar_sintactico=CCT, importancia=3))


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
    pos_media = len(matrix_dim)//2

    for (key, value) in importance_dict.items():
        if value['importancia'] % 2 != 0:
            axis_x = pos_media + (value['importancia'] - 1)
            matrix_dim[axis_x] += [0 for x in range(value['dimension']+2)]
        else:
            axis_x = pos_media - value['importancia']
            matrix_dim[axis_x] += [0 for x in range(value['dimension']+2)]

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
    for (key, value) in importance_dict.items():
        if value['importancia'] % 2 != 0:
            axis_x = pos_media + (value['importancia'] - 1)
            # obtener la posicion del primer 0 de la lista
            pos0 = matrix_dim[axis_x].index(0)
            pos.update({key: (value['dimension']//2 + pos0, axis_x - pos_media)})

            # reemplazar los 0s por 1s para range(value['dimension']+2)
            matrix_dim[axis_x][pos0:pos0+value['dimension']+2] = [1 for x in range(value['dimension']+2)]
        else:
            axis_x = pos_media - value['importancia']
            # obtener la posicion del primer 0 de la lista
            pos0 = matrix_dim[axis_x].index(0)
            pos.update({key: (value['dimension']//2 + pos0, axis_x - pos_media)})

            # reemplazar los 0s por 1s para range(value['dimension']+2)
            matrix_dim[axis_x][pos0:pos0 + value['dimension'] + 2] = [1 for x in range(value['dimension'] + 2)]

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
    None: '#000000'
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
        rectangle = Rectangle((x - rectangle_width / 2, y - 0.25), width=rectangle_width, height=0.5, color=red, zorder=2)
        ax.add_patch(rectangle)
        ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)

    elif pal.lugar_sintactico == CCL:
        polygon_radius = 0.06 * len(node) + 0.1
        polygon = RegularPolygon((x, y), numVertices=6, radius=polygon_radius, orientation=0, color=purple, zorder=2)
        ax.add_patch(polygon)
        ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)

    elif pal.lugar_sintactico == CCT:
        rectangle_width = 0.1 * len(node) + 0.2
        rectangle = Rectangle((x - rectangle_width / 2, y - 0.25), width=rectangle_width, height=0.5, color=green,
                              zorder=2)
        ax.add_patch(rectangle)
        ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)
    else:
        ellipse_width = 0.1 * len(node) + 0.2
        ellipse_height = 0.4
        ellipse = Ellipse((x, y), width=ellipse_width, height=ellipse_height, color='#000000', zorder=2)
        ax.add_patch(ellipse)
        ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)




# Dibujar aristas
for relation in list_relaciones:
    color = dict_color.get(relation.lugar_sintactico,'#000000')
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
