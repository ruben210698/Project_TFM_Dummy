
import re

from utils.Palabra import Palabra
from constants.direcciones_relaciones import CENTRO




class Relacion:
    id_actual = -9
    relaciones_dict = {}
    relaciones_dict_id = {}
    # TODO que no coja el lugar sintactico de la relacion, sino que coja el lugar sintactico de la palabra 2

    def __init__(self, texto, pal_origen, pal_dest, position_doc=9999, lugar_sintactico="", importancia = None, id=None,
                 tipo_morf = None):
        self.texto = self.limpiar_texto(texto)
        self.pal_origen = pal_origen
        self.pal_dest = pal_dest
        self.lugar_sintactico = lugar_sintactico
        self.tam_text = self.get_tam_texto(texto)
        self.cte_sum_x = 1
        self.cte_sum_y = 0
        self.id = id if id is not None else self.generar_id()
        self.importancia = importancia if importancia is not None else self.generar_importancia(pal_origen, pal_dest)
        self.position_doc = position_doc
        self.tipo_morf = tipo_morf
        self.direccion_actual = None
        self.has_been_plotted = False

        Relacion.relaciones_dict[self.texto] = self # TODO añadir la posicion del documento
        Relacion.relaciones_dict_id[self.id] = self
        Palabra.relaciones_dict_origen[self.pal_origen].append(self)
        Palabra.relaciones_dict_origen[self.pal_origen] = \
            Palabra.reordenar_importancia_list(Palabra.relaciones_dict_origen[self.pal_origen])
        pal_origen.refresh_grafos_aproximados()
        if pal_dest is not None:
            Palabra.relaciones_dict_destino[self.pal_dest].append(self)
            pal_dest.refresh_grafos_aproximados()

    @classmethod
    def generar_id(cls):
        cls.id_actual -= 1
        return cls.id_actual

    @classmethod
    def generar_importancia(cls, relacion1, relacion2):
        if relacion2 is None:
            return 1000 + relacion1.importancia
        return relacion1.importancia + relacion2.importancia

    @staticmethod
    def limpiar_texto(texto):
        texto_limpio = texto.lower()
        texto_limpio = re.sub(r'\W+', '', texto_limpio)
        return texto_limpio

    @staticmethod
    def get_tam_texto(texto):
        # Método que calcula la dimensión dependiendo del tamaño de la palabra
        return len(texto)//2 if len(texto) > 2 else 2

    def add_rel_dest(self, palabra_dest):
        Palabra.relaciones_dict_destino[self.pal_dest].append(palabra_dest)
        self.pal_dest = palabra_dest
        self.importancia = \
            self.importancia if self.importancia != 99 else self.generar_importancia(self.pal_origen, self.pal_dest)
        palabra_dest.refresh_grafos_aproximados()

    def __str__(self):
        return self.texto

    def to_create_Relacion_str(self):
        if self.tipo_morf is not None:
            return "list_relaciones.append(Relacion('" + self.texto + "', " + f"Palabra.palabras_dict.get('{self.pal_origen.txt_lema}-{self.pal_origen.position_doc}') " + ", " +  f"Palabra.palabras_dict.get('{self.pal_dest.txt_lema}-{self.pal_dest.position_doc}')" + f", position_doc={self.position_doc} "+", lugar_sintactico='" + self.lugar_sintactico + f"', importancia = {self.importancia}" + ", id=" + str(self.id) + ", tipo_morf = '" + str(self.tipo_morf) + "'))"
        else:
            return "list_relaciones.append(Relacion('" + self.texto + "', " + f"Palabra.palabras_dict.get('{self.pal_origen.txt_lema}-{self.pal_origen.position_doc}') " + ", " +  f"Palabra.palabras_dict.get('{self.pal_dest.txt_lema}-{self.pal_dest.position_doc}')" + f", position_doc={self.position_doc} "+", lugar_sintactico='" + self.lugar_sintactico + f"', importancia = {self.importancia}" + ", id=" + str(self.id) + "))"
    def delete_relation(self):
        try:
            if Palabra.relaciones_dict_origen.get(self.pal_origen) is not None:
                Palabra.relaciones_dict_origen[self.pal_origen].remove(self)
        except Exception as _:
            pass
        try:
            if self.pal_dest is not None and Palabra.relaciones_dict_destino.get(self.pal_dest) is not None:
                Palabra.relaciones_dict_destino[self.pal_dest].remove(self)
        except Exception as _:
            pass
        try:
            if Relacion.relaciones_dict_id.get(self.id) is not None:
                del Relacion.relaciones_dict_id[self.id]
        except Exception as _:
            pass


    def change_pal_origen(self, pal_origen):
        Palabra.relaciones_dict_origen[self.pal_origen].remove(self)
        Palabra.relaciones_dict_origen[pal_origen].append(self)
        Palabra.relaciones_dict_origen[pal_origen] = \
            Palabra.reordenar_importancia_list(Palabra.relaciones_dict_origen[pal_origen])
        self.pal_origen = pal_origen
        pal_origen.refresh_grafos_aproximados()

    def change_pal_dest(self, pal_dest):
        Palabra.relaciones_dict_destino[self.pal_dest].remove(self)
        Palabra.relaciones_dict_destino[pal_dest].append(self)
        self.pal_dest = pal_dest
        pal_dest.refresh_grafos_aproximados()
