
import re

from visualizacion.Palabra import Palabra

DIR_ABAJO = "abajo"
DIR_ARRIBA = "arriba"
DIR_DCHA = "derecha"
DIR_IZQ = "izquierda"

class Relacion:
    id_actual = -1
    relaciones_dict = {}

    def __init__(self, texto, pal_origen, pal_dest, lugar_sintactico="", id=None, importancia = None):
        self.texto = self.limpiar_texto(texto)
        self.pal_origen = pal_origen
        self.pal_dest = pal_dest
        self.lugar_sintactico = lugar_sintactico
        self.id = id if id is not None else self.generar_id()
        self.importancia = importancia if importancia is not None else self.generar_importancia(pal_origen, pal_dest)
        self.direccion = None

        Relacion.relaciones_dict[self.texto] = self
        Palabra.relaciones_dict_origen[self.pal_origen].append(self)
        Palabra.relaciones_dict_origen[self.pal_origen] = \
            Palabra.reordenar_importancia_list(Palabra.relaciones_dict_origen[self.pal_origen])
        Palabra.relaciones_dict_dest[self.pal_dest].append(self)

    @classmethod
    def generar_id(cls):
        cls.id_actual -= 1
        return cls.id_actual

    @classmethod
    def generar_importancia(cls, relacion1, relacion2):
        return relacion1.importancia + relacion2.importancia - 1

    @staticmethod
    def limpiar_texto(texto):
        texto_limpio = texto.lower()
        texto_limpio = re.sub(r'\W+', '', texto_limpio)
        return texto_limpio
