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

from grafico12 import print_graph

texto = "Ruben cocina hamburguesas en la Freidora de aire"
list_palabras = []
list_relaciones = []

list_palabras.append(Palabra('Ruben', 'PROPN', 'ROOT', 1, 99, 0, False, 'Ruben', 0))
list_palabras.append(Palabra('hamburguesas', 'ADJ', 'amod', 2, 99, 0, False, 'hamburguesa', 13))
#list_palabras.append(Palabra('pollo', 'ADJ', 'amod', 3, 99, 0, False, 'pollo', 13))
list_palabras.append(Palabra('Freidora', 'PROPN', 'nmod', 3, 99, 0, False, 'Freidora', 32))
list_palabras.append(Palabra('aire', 'PROPN', 'flat', 4, 99, 0, False, 'aire', 44))
list_relaciones.append(Relacion('cocina', Palabra.palabras_dict.get('Ruben'), Palabra.palabras_dict.get('hamburguesa'), 5, 'amod',  197, tipo_morf='VERB'))
list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('Freidora'), 17, 'nmod',  197))
list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('aire'), 17, 'flat',  197))
list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('Freidora'), 20, 'nmod',  197))
list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('aire'), 20, 'flat',  197))
list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('Freidora'), Palabra.palabras_dict.get('aire'), 38, 'flat',  197))
#list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('pollo'), 99, 'flat', 197))


# list_palabras.append(Palabra('Ruben', 'PROPN', 'ROOT', 1, 99, 0, False, 'Ruben', 0))
# list_palabras.append(Palabra('hamburguesas', 'ADJ', 'amod', 2, 99, 0, False, 'hamburguesa', 13))
# list_palabras.append(Palabra('Freidora', 'PROPN', 'nmod', 3, 99, 0, False, 'Freidora', 32))
# list_palabras.append(Palabra('aire', 'PROPN', 'flat', 4, 99, 0, False, 'aire', 44))
# list_palabras.append(Palabra('Mientras', 'ADV', 'advmod', 5, 99, 0, False, 'mientras', 50))
# list_palabras.append(Palabra('amigo', 'NOUN', 'nsubj', 6, 99, 0, False, 'amigo', 63))
# list_palabras.append(Palabra('escena', 'NOUN', 'obj', 7, 99, 0, False, 'escena', 78))
# list_relaciones.append(Relacion('cocina', Palabra.palabras_dict.get('Ruben') , Palabra.palabras_dict.get('hamburguesa'), '', -2, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('hamburguesa') , Palabra.palabras_dict.get('Freidora'), '', -3, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('hamburguesa') , Palabra.palabras_dict.get('aire'), '', -4, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('hamburguesa') , Palabra.palabras_dict.get('Freidora'), '', -5, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('hamburguesa') , Palabra.palabras_dict.get('aire'), '', -6, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('Freidora') , Palabra.palabras_dict.get('aire'), '', -7, 197))
# list_relaciones.append(Relacion('graba', Palabra.palabras_dict.get('mientras') , Palabra.palabras_dict.get('amigo'), '', -8, 197))
# list_relaciones.append(Relacion('graba', Palabra.palabras_dict.get('mientras') , Palabra.palabras_dict.get('escena'), '', -9, 197))

# list_palabras.append(Palabra('Ruben', 'PROPN', 'nsubj', 1, 99, 0, False, 'Ruben', 0))
# list_palabras.append(Palabra('hamburguesas', 'ADJ', 'obj', 2, 99, 0, False, 'hamburguesa', 13))
# list_palabras.append(Palabra('carne', 'NOUN', 'nmod', 3, 99, 0, False, 'carne', 30))
# list_palabras.append(Palabra('picada', 'ADJ', 'amod', 4, 99, 0, False, 'picado', 36))
# list_palabras.append(Palabra('cebolla', 'ADJ', 'conj', 5, 99, 0, False, 'cebollo', 45))
# list_palabras.append(Palabra('sartén', 'NOUN', 'obl', 6, 99, 0, False, 'sartén', 59))
# list_palabras.append(Palabra('aceite', 'NOUN', 'nsubj', 7, 99, 0, False, 'aceite', 79))
# list_relaciones.append(Relacion('cocina', Palabra.palabras_dict.get('Ruben') , Palabra.palabras_dict.get('hamburguesa'), '', -2, 197))
# list_relaciones.append(Relacion('cocina', Palabra.palabras_dict.get('Ruben') , Palabra.palabras_dict.get('cebollo'), '', -3, 197))
# list_relaciones.append(Relacion('con', Palabra.palabras_dict.get('hamburguesa') , Palabra.palabras_dict.get('carne'), '', -4, 197))
# list_relaciones.append(Relacion('con', Palabra.palabras_dict.get('hamburguesa') , Palabra.palabras_dict.get('picado'), '', -5, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('sartén'), '', -6, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('sartén'), '', -7, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('sartén'), '', -8, 197))
# list_relaciones.append(Relacion('tiene', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('aceite'), '', -9, 197))
# list_relaciones.append(Relacion('tiene', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('sartén'), '', -10, 197))
# list_relaciones.append(Relacion('hirviendo', Palabra.palabras_dict.get('Ruben') , Palabra.palabras_dict.get('cocina'), '', -22, 197))










print_graph(texto, list_palabras, list_relaciones)

