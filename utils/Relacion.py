
import re

from utils.Palabra import Palabra

DIR_ABAJO = "abajo"
DIR_ARRIBA = "arriba"
DIR_DCHA = "derecha"
DIR_IZQ = "izquierda"

class Relacion:
    id_actual = -1
    relaciones_dict = {}
    relaciones_dict_id = {}
    # TODO que no coja el lugar sintactico de la relacion, sino que coja el lugar sintactico de la palabra 2

    def __init__(self, texto, pal_origen, pal_dest, position_doc=9999, lugar_sintactico="", id=None, importancia = None):
        self.texto = self.limpiar_texto(texto)
        self.pal_origen = pal_origen
        self.pal_dest = pal_dest
        self.lugar_sintactico = lugar_sintactico
        self.tam_texto = self.get_tam_texto(texto)
        self.id = id if id is not None else self.generar_id()
        self.importancia = importancia if importancia is not None else self.generar_importancia(pal_origen, pal_dest)
        self.direccion = None
        self.position_doc = position_doc

        Relacion.relaciones_dict[self.texto] = self
        Relacion.relaciones_dict_id[self.id] = self
        Palabra.relaciones_dict_origen[self.pal_origen].append(self)
        Palabra.relaciones_dict_origen[self.pal_origen] = \
            Palabra.reordenar_importancia_list(Palabra.relaciones_dict_origen[self.pal_origen])
        if pal_dest is not None:
            Palabra.relaciones_dict_dest[self.pal_dest].append(self)

    @classmethod
    def generar_id(cls):
        cls.id_actual -= 1
        return cls.id_actual

    @classmethod
    def generar_importancia(cls, relacion1, relacion2):
        if relacion2 is None:
            return 99
        return relacion1.importancia + relacion2.importancia - 1

    @staticmethod
    def limpiar_texto(texto):
        texto_limpio = texto.lower()
        texto_limpio = re.sub(r'\W+', '', texto_limpio)
        return texto_limpio

    @staticmethod
    def get_tam_texto(texto):
        # Método que calcula la dimensión dependiendo del tamaño de la palabra
        return len(texto)//3 if len(texto) > 3 else 1

    def add_rel_dest(self, palabra_dest):
        Palabra.relaciones_dict_dest[self.pal_dest].append(palabra_dest)
        self.pal_dest = palabra_dest
        self.importancia = \
            self.importancia if self.importancia != 99 else self.generar_importancia(self.pal_origen, self.pal_dest)

    def __str__(self):
        return self.texto

    def to_create_Relacion_str(self):
        return "list_relaciones.append(Relacion('" + self.texto + "', " + f"Palabra.palabras_dict.get('{self.pal_origen.txt_lema}') " + ", " +  f"Palabra.palabras_dict.get('{self.pal_dest.txt_lema}')" + ", '" + self.lugar_sintactico + "', " + str(self.id) + ", " + str(self.importancia) + "))"

    def delete_relation(self):
        Palabra.relaciones_dict_origen[self.pal_origen].remove(self)
        if self.pal_dest is not None:
            Palabra.relaciones_dict_dest[self.pal_dest].remove(self)
        del Relacion.relaciones_dict_id[self.id]
