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

# texto = "Ruben cocina hamburguesas en la Freidora de aire"
# list_palabras = []
# list_relaciones = []
#
# list_palabras.append(Palabra('Ruben', 'PROPN', 'ROOT', 1, 99, 0, False, 'Ruben', 0))
# list_palabras.append(Palabra('hamburguesas', 'ADJ', 'amod', 2, 99, 0, False, 'hamburguesa', 13))
# #list_palabras.append(Palabra('pollo', 'ADJ', 'amod', 3, 99, 0, False, 'pollo', 13))
# list_palabras.append(Palabra('Freidora', 'PROPN', 'nmod', 3, 99, 0, False, 'Freidora', 32))
# list_palabras.append(Palabra('aire', 'PROPN', 'flat', 4, 99, 0, False, 'aire', 44))
# list_relaciones.append(Relacion('cocina', Palabra.palabras_dict.get('Ruben'), Palabra.palabras_dict.get('hamburguesa'), 5, 'amod',  197, tipo_morf='VERB'))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('Freidora'), 17, 'nmod',  197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('aire'), 17, 'flat',  197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('Freidora'), 20, 'nmod',  197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('aire'), 20, 'flat',  197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('Freidora'), Palabra.palabras_dict.get('aire'), 38, 'flat',  197))
# #list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('hamburguesa'), Palabra.palabras_dict.get('pollo'), 99, 'flat', 197))













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


texto = "Ruben cocina hamburguesas en la Freidora de aire"
list_palabras = []
list_relaciones = []

def test1():
    list_palabras.append(Palabra('Ruben', 'PROPN', 'nsubj', 1, 99, 0, False, 'Ruben', 0))
    list_palabras.append(Palabra('hamburguesas', 'ADJ', 'obj', 2, 99, 0, False, 'hamburguesa', 13))
    list_palabras.append(Palabra('carne', 'NOUN', 'nmod', 3, 99, 0, False, 'carne', 30))
    list_palabras.append(Palabra('picada', 'ADJ', 'amod', 4, 99, 0, False, 'picado', 36))
    list_palabras.append(Palabra('cebolla', 'ADJ', 'conj', 5, 99, 0, False, 'cebollo', 45))
    list_palabras.append(Palabra('sartén', 'NOUN', 'obl', 6, 99, 0, False, 'sartén', 59))
    list_palabras.append(Palabra('aceite', 'NOUN', 'nsubj', 7, 99, 0, False, 'aceite', 79))
    list_relaciones.append(Relacion('cocina', Palabra.palabras_dict.get('Ruben') , Palabra.palabras_dict.get('hamburguesa'), '', -2, 197))
    list_relaciones.append(Relacion('cocina', Palabra.palabras_dict.get('Ruben') , Palabra.palabras_dict.get('cebollo'), '', -3, 197))
    list_relaciones.append(Relacion('con', Palabra.palabras_dict.get('hamburguesa') , Palabra.palabras_dict.get('carne'), '', -4, 197))
    list_relaciones.append(Relacion('con', Palabra.palabras_dict.get('hamburguesa') , Palabra.palabras_dict.get('picado'), '', -5, 197))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('sartén'), '', -6, 197))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('sartén'), '', -7, 197))
    list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('sartén'), '', -8, 197))
    list_relaciones.append(Relacion('tiene', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('aceite'), '', -9, 197))
    list_relaciones.append(Relacion('tiene', Palabra.palabras_dict.get('cebollo') , Palabra.palabras_dict.get('sartén'), '', -10, 197))
    list_relaciones.append(Relacion('hirviendo', Palabra.palabras_dict.get('Ruben') , Palabra.palabras_dict.get('cocina'), '', -22, 197))














# list_palabras.append(Palabra('dinastía', 'NOUN', 'nsubj', 1, 99, 0, False, 'dinastía', 3))
# list_palabras.append(Palabra('Austrias', 'PROPN', 'nmod', 2, 99, 0, False, 'Austrias', 19))
# list_palabras.append(Palabra('España', 'PROPN', 'obj', 3, 99, 0, False, 'España', 36))
# list_palabras.append(Palabra('siglo', 'NOUN', 'obl', 4, 99, 0, False, 'siglo', 52))
# list_palabras.append(Palabra('XVI', 'NOUN', 'compound', 5, 99, 0, False, 'xvi', 58))
# list_palabras.append(Palabra('siglo', 'NOUN', 'obl', 6, 99, 0, False, 'siglo', 71))
# list_palabras.append(Palabra('XVII', 'NOUN', 'compound', 7, 99, 0, False, 'xvii', 77))
# list_palabras.append(Palabra('reinado', 'NOUN', 'obl', 8, 99, 0, False, 'reinado', 94))
# list_palabras.append(Palabra('país', 'NOUN', 'nsubj', 9, 99, 0, False, 'país', 106))
# list_palabras.append(Palabra('época', 'NOUN', 'obj', 10, 99, 0, False, 'época', 127))
# list_palabras.append(Palabra('esplendor', 'NOUN', 'nmod', 11, 99, 0, False, 'esplendor', 136))
# list_palabras.append(Palabra('decadencia', 'NOUN', 'conj', 12, 99, 0, False, 'decadencia', 148))
# list_palabras.append(Palabra('monarcas', 'NOUN', 'nsubj', 13, 99, 0, False, 'monarca', 164))
# list_palabras.append(Palabra('austriacos', 'ADJ', 'amod', 14, 99, 0, False, 'austriaco', 173))
# list_palabras.append(Palabra('Carlos', 'PROPN', 'appos', 15, 99, 0, False, 'Carlos', 197))
# list_palabras.append(Palabra('I', 'PROPN', 'flat', 16, 99, 0, False, 'I', 204))
# list_palabras.append(Palabra('Felipe', 'PROPN', 'conj', 17, 99, 0, False, 'Felipe', 208))
# list_palabras.append(Palabra('II', 'PROPN', 'flat', 18, 99, 0, False, 'II', 215))
# list_palabras.append(Palabra('territorio', 'NOUN', 'obj', 19, 99, 0, False, 'territorio', 232))
# list_palabras.append(Palabra('español', 'ADJ', 'amod', 20, 99, 0, False, 'español', 243))
# list_palabras.append(Palabra('conquista', 'NOUN', 'obl', 21, 99, 0, False, 'conquista', 263))
# list_palabras.append(Palabra('América', 'PROPN', 'nmod', 22, 99, 0, False, 'América', 276))
# list_palabras.append(Palabra('anexión', 'NOUN', 'conj', 23, 99, 0, False, 'anexión', 289))
# list_palabras.append(Palabra('Portugal', 'PROPN', 'nmod', 24, 99, 0, False, 'Portugal', 300))
# list_palabras.append(Palabra('embargo', 'NOUN', 'fixed', 25, 99, 0, False, 'embargo', 314))
# list_palabras.append(Palabra('también', 'ADV', 'advmod', 26, 99, 0, False, 'también', 323))
# list_palabras.append(Palabra('fueron', 'AUX', 'cop', 27, 99, 0, False, 'ser', 331))
# list_palabras.append(Palabra('responsables', 'NOUN', 'ROOT', 28, 99, 0, False, 'responsable', 338))
# list_palabras.append(Palabra('Inquisición', 'PROPN', 'nmod', 29, 99, 0, False, 'Inquisición', 357))
# list_palabras.append(Palabra('española', 'ADJ', 'amod', 30, 99, 0, False, 'español', 369))
# list_palabras.append(Palabra('expulsión', 'NOUN', 'conj', 31, 99, 0, False, 'expulsión', 386))
# list_palabras.append(Palabra('judíos', 'NOUN', 'nmod', 32, 99, 0, False, 'judío', 403))
# list_palabras.append(Palabra('falta', 'NOUN', 'nsubj', 33, 99, 0, False, 'falta', 414))
# list_palabras.append(Palabra('recursos', 'NOUN', 'nmod', 34, 99, 0, False, 'recurso', 423))
# list_palabras.append(Palabra('guerras', 'NOUN', 'conj', 35, 99, 0, False, 'guerra', 438))
# list_palabras.append(Palabra('Europa', 'PROPN', 'nmod', 36, 99, 0, False, 'Europa', 449))
# list_palabras.append(Palabra('declive', 'NOUN', 'obj', 37, 99, 0, False, 'declive', 473))
# list_palabras.append(Palabra('monarquía', 'NOUN', 'nmod', 38, 99, 0, False, 'monarquía', 487))
# list_palabras.append(Palabra('llegada', 'NOUN', 'obl', 39, 99, 0, False, 'llegada', 517))
# list_palabras.append(Palabra('dinastía', 'NOUN', 'nmod', 40, 99, 0, False, 'dinastía', 531))
# list_palabras.append(Palabra('Borbones', 'PROPN', 'nmod', 41, 99, 0, False, 'Borbones', 547))
# list_palabras.append(Palabra('siglo', 'NOUN', 'nmod', 42, 99, 0, False, 'siglo', 562))
# list_palabras.append(Palabra('XVIII', 'NOUN', 'compound', 43, 99, 0, False, 'xviii', 568))
# list_palabras.append(Palabra('legado', 'NOUN', 'nsubj', 44, 99, 0, False, 'legado', 578))
# list_palabras.append(Palabra('Austrias', 'PROPN', 'nmod', 45, 99, 0, False, 'Austrias', 592))
# list_palabras.append(Palabra('España', 'PROPN', 'nmod', 46, 99, 0, False, 'España', 604))
# list_palabras.append(Palabra('puede', 'AUX', 'aux', 47, 99, 0, False, 'poder', 614))
# list_palabras.append(Palabra('arquitectura', 'NOUN', 'obl', 48, 99, 0, False, 'arquitectura', 630))
# list_palabras.append(Palabra('arte', 'NOUN', 'conj', 49, 99, 0, False, 'arte', 645))
# list_palabras.append(Palabra('especialmente', 'ADV', 'advmod', 50, 99, 0, False, 'especialmente', 651))
# list_palabras.append(Palabra('Madrid', 'PROPN', 'nmod', 51, 99, 0, False, 'Madrid', 668))
# list_palabras.append(Palabra('ciudades', 'NOUN', 'conj', 52, 99, 0, False, 'ciudad', 684))
# list_palabras.append(Palabra('andaluzas', 'NOUN', 'amod', 53, 99, 0, False, 'andaluza', 693))
# list_palabras.append(Palabra('Granada', 'PROPN', 'nmod', 54, 99, 0, False, 'Granada', 706))
# list_palabras.append(Palabra('Córdoba', 'PROPN', 'conj', 55, 99, 0, False, 'Córdoba', 716))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('dinastía') , Palabra.palabras_dict.get('Austrias'), '', -2, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('dinastía') , Palabra.palabras_dict.get('Austrias'), '', -3, 197))
# list_relaciones.append(Relacion('los', Palabra.palabras_dict.get('dinastía') , Palabra.palabras_dict.get('Austrias'), '', -4, 197))
# list_relaciones.append(Relacion('gobernó', Palabra.palabras_dict.get('dinastía') , Palabra.palabras_dict.get('España'), '', -5, 197))
# list_relaciones.append(Relacion('gobernó', Palabra.palabras_dict.get('dinastía') , Palabra.palabras_dict.get('siglo'), '', -6, 197))
# list_relaciones.append(Relacion('gobernó', Palabra.palabras_dict.get('dinastía') , Palabra.palabras_dict.get('siglo'), '', -7, 197))
# list_relaciones.append(Relacion('desde', Palabra.palabras_dict.get('xvi') , Palabra.palabras_dict.get('siglo'), '', -8, 197))
# list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('xvi') , Palabra.palabras_dict.get('siglo'), '', -9, 197))
# list_relaciones.append(Relacion('hasta', Palabra.palabras_dict.get('xvii') , Palabra.palabras_dict.get('siglo'), '', -10, 197))
# list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('xvii') , Palabra.palabras_dict.get('siglo'), '', -11, 197))
# list_relaciones.append(Relacion('experimentó', Palabra.palabras_dict.get('reinado') , Palabra.palabras_dict.get('país'), '', -12, 197))
# list_relaciones.append(Relacion('experimentó', Palabra.palabras_dict.get('reinado') , Palabra.palabras_dict.get('época'), '', -13, 197))
# list_relaciones.append(Relacion('una', Palabra.palabras_dict.get('época') , Palabra.palabras_dict.get('esplendor'), '', -14, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('época') , Palabra.palabras_dict.get('esplendor'), '', -15, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('época') , Palabra.palabras_dict.get('decadencia'), '', -16, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('esplendor') , Palabra.palabras_dict.get('decadencia'), '', -17, 197))
# list_relaciones.append(Relacion('los', Palabra.palabras_dict.get('monarca') , Palabra.palabras_dict.get('austriaco'), '', -18, 197))
# list_relaciones.append(Relacion('ellos', Palabra.palabras_dict.get('monarca') , Palabra.palabras_dict.get('Carlos'), '', -19, 197))
# list_relaciones.append(Relacion('ellos', Palabra.palabras_dict.get('monarca') , Palabra.palabras_dict.get('austriaco'), '', -20, 197))
# list_relaciones.append(Relacion('ellos', Palabra.palabras_dict.get('monarca') , Palabra.palabras_dict.get('I'), '', -21, 197))
# list_relaciones.append(Relacion('ellos', Palabra.palabras_dict.get('monarca') , Palabra.palabras_dict.get('Felipe'), '', -22, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('Carlos') , Palabra.palabras_dict.get('Felipe'), '', -23, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('Carlos') , Palabra.palabras_dict.get('II'), '', -24, 197))
# list_relaciones.append(Relacion('ampliaron', Palabra.palabras_dict.get('monarca') , Palabra.palabras_dict.get('territorio'), '', -25, 197))
# list_relaciones.append(Relacion('ampliaron', Palabra.palabras_dict.get('monarca') , Palabra.palabras_dict.get('conquista'), '', -26, 197))
# list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('territorio') , Palabra.palabras_dict.get('español'), '', -27, 197))
# list_relaciones.append(Relacion('mediante', Palabra.palabras_dict.get('conquista') , Palabra.palabras_dict.get('América'), '', -28, 197))
# list_relaciones.append(Relacion('mediante', Palabra.palabras_dict.get('conquista') , Palabra.palabras_dict.get('anexión'), '', -29, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('conquista') , Palabra.palabras_dict.get('América'), '', -30, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('conquista') , Palabra.palabras_dict.get('anexión'), '', -31, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('conquista') , Palabra.palabras_dict.get('América'), '', -32, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('conquista') , Palabra.palabras_dict.get('anexión'), '', -33, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('conquista') , Palabra.palabras_dict.get('Portugal'), '', -34, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('conquista') , Palabra.palabras_dict.get('anexión'), '', -35, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('conquista') , Palabra.palabras_dict.get('Portugal'), '', -36, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('anexión') , Palabra.palabras_dict.get('Portugal'), '', -37, 197))
# list_relaciones.append(Relacion('sin', Palabra.palabras_dict.get('embargo') , Palabra.palabras_dict.get('responsable'), '', -38, 197))
# list_relaciones.append(Relacion('sin', Palabra.palabras_dict.get('embargo') , Palabra.palabras_dict.get('también'), '', -39, 197))
# list_relaciones.append(Relacion('sin', Palabra.palabras_dict.get('embargo') , Palabra.palabras_dict.get('ser'), '', -40, 197))
# list_relaciones.append(Relacion('sin', Palabra.palabras_dict.get('embargo') , Palabra.palabras_dict.get('Inquisición'), '', -41, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('Inquisición'), '', -42, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('español'), '', -43, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('expulsión'), '', -44, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('Inquisición'), '', -45, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('español'), '', -46, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('expulsión'), '', -47, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('Inquisición') , Palabra.palabras_dict.get('expulsión'), '', -48, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('Inquisición') , Palabra.palabras_dict.get('judío'), '', -49, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('Inquisición') , Palabra.palabras_dict.get('expulsión'), '', -50, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('Inquisición') , Palabra.palabras_dict.get('judío'), '', -51, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('Inquisición') , Palabra.palabras_dict.get('expulsión'), '', -52, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('Inquisición') , Palabra.palabras_dict.get('judío'), '', -53, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('expulsión') , Palabra.palabras_dict.get('judío'), '', -54, 197))
# list_relaciones.append(Relacion('los', Palabra.palabras_dict.get('expulsión') , Palabra.palabras_dict.get('judío'), '', -55, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('falta') , Palabra.palabras_dict.get('recurso'), '', -56, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('falta') , Palabra.palabras_dict.get('guerra'), '', -57, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('falta') , Palabra.palabras_dict.get('recurso'), '', -58, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('falta') , Palabra.palabras_dict.get('guerra'), '', -59, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('falta') , Palabra.palabras_dict.get('Europa'), '', -60, 197))
# list_relaciones.append(Relacion('las', Palabra.palabras_dict.get('falta') , Palabra.palabras_dict.get('guerra'), '', -61, 197))
# list_relaciones.append(Relacion('las', Palabra.palabras_dict.get('falta') , Palabra.palabras_dict.get('Europa'), '', -62, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('guerra') , Palabra.palabras_dict.get('Europa'), '', -63, 197))
# list_relaciones.append(Relacion('contribuyeron', Palabra.palabras_dict.get('falta') , Palabra.palabras_dict.get('declive'), '', -64, 197))
# list_relaciones.append(Relacion('al', Palabra.palabras_dict.get('declive') , Palabra.palabras_dict.get('monarquía'), '', -65, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('declive') , Palabra.palabras_dict.get('monarquía'), '', -66, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('declive') , Palabra.palabras_dict.get('monarquía'), '', -67, 197))
# list_relaciones.append(Relacion('terminó', Palabra.palabras_dict.get('declive') , Palabra.palabras_dict.get('llegada'), '', -68, 197))
# list_relaciones.append(Relacion('terminó', Palabra.palabras_dict.get('declive') , Palabra.palabras_dict.get('monarquía'), '', -69, 197))
# list_relaciones.append(Relacion('terminó', Palabra.palabras_dict.get('declive') , Palabra.palabras_dict.get('dinastía'), '', -70, 197))
# list_relaciones.append(Relacion('terminó', Palabra.palabras_dict.get('declive') , Palabra.palabras_dict.get('siglo'), '', -71, 197))
# list_relaciones.append(Relacion('con', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('dinastía'), '', -72, 197))
# list_relaciones.append(Relacion('con', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('siglo'), '', -73, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('dinastía'), '', -74, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('siglo'), '', -75, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('dinastía'), '', -76, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('Borbones'), '', -77, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('dinastía'), '', -78, 197))
# list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('Borbones'), '', -79, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('dinastía') , Palabra.palabras_dict.get('Borbones'), '', -80, 197))
# list_relaciones.append(Relacion('los', Palabra.palabras_dict.get('dinastía') , Palabra.palabras_dict.get('Borbones'), '', -81, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('siglo'), '', -82, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('xviii'), '', -83, 197))
# list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('siglo'), '', -84, 197))
# list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('llegada') , Palabra.palabras_dict.get('xviii'), '', -85, 197))
# list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('Austrias'), '', -86, 197))
# list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('España'), '', -87, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('Austrias'), '', -88, 197))
# list_relaciones.append(Relacion('los', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('Austrias'), '', -89, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('España'), '', -90, 197))
# list_relaciones.append(Relacion('ver', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('poder'), '', -91, 197))
# list_relaciones.append(Relacion('ver', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('arquitectura'), '', -92, 197))
# list_relaciones.append(Relacion('ver', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('especialmente'), '', -93, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('arte'), '', -94, 197))
# list_relaciones.append(Relacion('su', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('arte'), '', -95, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('arte'), '', -96, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('Madrid'), '', -97, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('ciudad'), '', -98, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('ciudad'), '', -99, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('andaluza'), '', -100, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('Granada'), '', -101, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('ciudad'), '', -102, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('andaluza'), '', -103, 197))
# list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('Granada'), '', -104, 197))
# list_relaciones.append(Relacion('las', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('ciudad'), '', -105, 197))
# list_relaciones.append(Relacion('las', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('andaluza'), '', -106, 197))
# list_relaciones.append(Relacion('las', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('Granada'), '', -107, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('ciudad') , Palabra.palabras_dict.get('Granada'), '', -108, 197))
# list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('ciudad') , Palabra.palabras_dict.get('Córdoba'), '', -109, 197))
# list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('Granada') , Palabra.palabras_dict.get('Córdoba'), '', -110, 197))
# list_relaciones.append(Relacion('su', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('arte'), '', -206, 197))

def test4():
    list_palabras.append(Palabra('Austrias', 'PROPN', 'nsubj', 1, 99, 0, False, 'Austrias', 4))
    list_palabras.append(Palabra('España', 'PROPN', 'obj', 2, 99, 0, False, 'España', 24))
    list_palabras.append(Palabra('siglo', 'NOUN', 'obl', 3, 99, 0, False, 'siglo', 37))
    list_palabras.append(Palabra('XVI', 'NOUN', 'compound', 4, 99, 0, False, 'xvi', 43))
    list_palabras.append(Palabra('XVII', 'NOUN', 'conj', 5, 99, 0, False, 'xvii', 49))
    list_palabras.append(Palabra('territorio', 'NOUN', 'obj', 6, 99, 0, False, 'territorio', 68))
    list_palabras.append(Palabra('también', 'ADV', 'advmod', 7, 99, 0, False, 'también', 84))
    list_palabras.append(Palabra('responsables', 'ADJ', 'conj', 8, 99, 0, False, 'responsable', 92))
    list_palabras.append(Palabra('Inquisición', 'PROPN', 'nmod', 9, 99, 0, False, 'Inquisición', 111))
    list_palabras.append(Palabra('expulsión', 'NOUN', 'conj', 10, 99, 0, False, 'expulsión', 128))
    list_palabras.append(Palabra('judíos', 'NOUN', 'nmod', 11, 99, 0, False, 'judío', 141))
    list_palabras.append(Palabra('legado', 'NOUN', 'nsubj', 12, 99, 0, False, 'legado', 152))
    list_palabras.append(Palabra('arquitectura', 'NOUN', 'obl', 13, 99, 0, False, 'arquitectura', 171))
    list_palabras.append(Palabra('arte', 'NOUN', 'conj', 14, 99, 0, False, 'arte', 189))
    list_palabras.append(Palabra('especialmente', 'ADV', 'advmod', 15, 99, 0, False, 'especialmente', 195))
    list_palabras.append(Palabra('Madrid', 'PROPN', 'nmod', 16, 99, 0, False, 'Madrid', 212))
    list_palabras.append(Palabra('Granada', 'PROPN', 'conj', 17, 99, 0, False, 'Granada', 220))
    list_palabras.append(Palabra('Córdoba', 'PROPN', 'conj', 18, 99, 0, False, 'Córdoba', 230))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias') , Palabra.palabras_dict.get('España'), '', -2, 197))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias') , Palabra.palabras_dict.get('siglo'), '', -3, 197))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias') , Palabra.palabras_dict.get('responsable'), '', -4, 197))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvi'), '', -5, 197))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvii'), '', -6, 197))
    list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvi'), '', -7, 197))
    list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvii'), '', -8, 197))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvii'), '', -9, 197))
    list_relaciones.append(Relacion('pero', Palabra.palabras_dict.get('también') , Palabra.palabras_dict.get('responsable'), '', -10, 197))
    list_relaciones.append(Relacion('pero', Palabra.palabras_dict.get('también') , Palabra.palabras_dict.get('Inquisición'), '', -11, 197))
    list_relaciones.append(Relacion('pero', Palabra.palabras_dict.get('también') , Palabra.palabras_dict.get('expulsión'), '', -12, 197))
    list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('Inquisición'), '', -13, 197))
    list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('Inquisición'), '', -14, 197))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('expulsión'), '', -15, 197))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('judío'), '', -16, 197))
    list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('expulsión'), '', -17, 197))
    list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('judío'), '', -18, 197))
    list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('expulsión') , Palabra.palabras_dict.get('judío'), '', -19, 197))
    list_relaciones.append(Relacion('ve', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('arquitectura'), '', -20, 197))
    list_relaciones.append(Relacion('ve', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('especialmente'), '', -21, 197))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('arte'), '', -22, 197))
    list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('arte'), '', -23, 197))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('arte'), '', -24, 197))
    list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('arte'), '', -25, 197))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('especialmente') , Palabra.palabras_dict.get('Madrid'), '', -26, 197))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('Madrid') , Palabra.palabras_dict.get('Córdoba'), '', -27, 197))
    testo = "Durante el siglo XVI y XVII, las Austrias gobernaron España y fueron responsables de la Inquisición y la expulsión de los judíos. A pesar de eso, su legado en la arquitectura y el arte, especialmente en Madrid, es visible en la ciudad y en otras regiones como Granada y Córdoba."


def text5():
    texto = "Los Austrias gobernaron España en el siglo XVI y XVII, responsables también de la Inquisición, expulsión de judíos. Su legado: arquitectura y arte en Madrid, Córdoba."
    list_palabras.append(Palabra('Austrias', 'PROPN', 'nsubj', 1, 99, 0, False, 'Austrias', 4))
    list_palabras.append(Palabra('España', 'PROPN', 'obj', 2, 99, 0, False, 'España', 24))
    list_palabras.append(Palabra('siglo', 'NOUN', 'obl', 3, 99, 0, False, 'siglo', 37))
    list_palabras.append(Palabra('XVI', 'NOUN', 'compound', 4, 99, 0, False, 'xvi', 43))
    list_palabras.append(Palabra('XVII', 'NOUN', 'conj', 5, 99, 0, False, 'xvii', 49))
    list_palabras.append(Palabra('responsables', 'ADJ', 'obj', 6, 99, 0, False, 'responsable', 55))
    list_palabras.append(Palabra('también', 'ADV', 'advmod', 7, 99, 0, False, 'también', 68))
    list_palabras.append(Palabra('Inquisición', 'PROPN', 'nmod', 8, 99, 0, False, 'Inquisición', 82))
    list_palabras.append(Palabra('expulsión', 'NOUN', 'obj', 9, 99, 0, False, 'expulsión', 95))
    list_palabras.append(Palabra('judíos', 'NOUN', 'nmod', 10, 99, 0, False, 'judío', 108))
    list_palabras.append(Palabra('legado', 'NOUN', 'ROOT', 11, 99, 0, False, 'legado', 119))
    list_palabras.append(Palabra('arquitectura', 'NOUN', 'appos', 12, 99, 0, False, 'arquitectura', 127))
    list_palabras.append(Palabra('arte', 'NOUN', 'conj', 13, 99, 0, False, 'arte', 142))
    list_palabras.append(Palabra('Madrid', 'PROPN', 'nmod', 14, 99, 0, False, 'Madrid', 150))
    list_palabras.append(Palabra('Córdoba', 'PROPN', 'appos', 15, 99, 0, False, 'Córdoba', 158))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias') , Palabra.palabras_dict.get('España'), '', -2, 197))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias') , Palabra.palabras_dict.get('siglo'), '', -3, 197))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias') , Palabra.palabras_dict.get('responsable'), '', -4, 197))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias') , Palabra.palabras_dict.get('expulsión'), '', -5, 197))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvi'), '', -6, 197))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvii'), '', -7, 197))
    list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvi'), '', -8, 197))
    list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvii'), '', -9, 197))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('siglo') , Palabra.palabras_dict.get('xvii'), '', -10, 197))
    list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('también'), '', -11, 197))
    list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('responsable') , Palabra.palabras_dict.get('Inquisición'), '', -12, 197))
    list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('también') , Palabra.palabras_dict.get('Inquisición'), '', -13, 197))
    list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('expulsión') , Palabra.palabras_dict.get('judío'), '', -14, 197))
    list_relaciones.append(Relacion('su', Palabra.palabras_dict.get('legado') , Palabra.palabras_dict.get('arquitectura'), '', -15, 197))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('arte'), '', -16, 197))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('arquitectura') , Palabra.palabras_dict.get('Madrid'), '', -17, 197))


text5()

print_graph(texto, list_palabras, list_relaciones)

