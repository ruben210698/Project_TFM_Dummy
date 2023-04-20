"""
Clase Palabra:
texto: Una cadena de caracteres que representan una palabra.
tipo: Una cadena de caracteres que indica el tipo de palabra (sustantivo, verbo, adjetivo, etc.).
syntactic_place: Una cadena de caracteres que indica la posición sintáctica de una palabra (sujeto, objeto directo, objeto indirecto, etc.).
relaciones: un diccionario que contiene palabras y tipos de relaciones relacionadas con la palabra actual (por ejemplo, si la palabra actual es un verbo, la palabra relacionada puede ser un sujeto directo y un objeto, con una etiqueta que indica cuál es cuál).
id: Un identificador numérico generado automáticamente para cada palabra.
Importancia: un valor numérico que indica la importancia de la palabra en el texto (por ejemplo, la cantidad de veces que aparece la palabra en el texto).

"""
import re
from constants.direcciones_relaciones import CENTRO

"""
¿Por qué hay un id_actual que a veces es autoincremental y a veces no?
Pues porque hay palabras como verbos, adjetivos o sustantivos que se van a repetir en la oración pero
no son lo mismo.
Sin embargo, si hay palabras iguales como nombres propios, nombres de ciudades...
De esta forma, palabras que se repiten y no queremos que sean iguales en el grafo, serán autoimcrementales
y palabras que se repitan y queramos que se relacionen, se guardarán con el id como su hash y serán iguales.
"""


class Palabra:
    id_actual = 9
    palabras_dict = {}
    relaciones_dict_origen = {}
    relaciones_dict_destino = {}

    def __init__(self, texto, tipo, lugar_sintactico, id=None, importancia=None, num_relaciones=0, autoincremental=True,
                 txt_lema=None, position_doc=9999):

        self.texto = texto
        self.txt_lema = txt_lema if txt_lema is not None else self.limpiar_texto(texto)
        self.tipo = tipo
        self.lugar_sintactico = lugar_sintactico
        self.id = id if id is not None else self.generar_id(texto, autoincremental)
        # A menor valor de imporancia, mayor importancia tiene. Valor max=1
        if importancia is None:
            self.importancia = 1000 + int(position_doc)
        else:
            self.importancia = importancia
        self.num_relaciones = num_relaciones
        self.dimension = self.get_dimension(texto)
        self.cte_sum_x = 5
        self.cte_sum_y = 2
        self.dimension_y = 1
        self.has_been_plotted = False
        self.position_doc = position_doc
        self.figura = None
        self.multiplicador_borde_figura = None
        self.tam_eje_y_figura = None
        self.pos_x = None
        self.pos_y = None
        self.list_texto_enumeracion = []
        self.is_enumeracion = False

        self.numero_grafos = -1
        self.grafos_aproximados = []
        self.direccion_origen = CENTRO
        self.pos_actual_recorrer_dir_relaciones = 0
        self.lista_direcciones_orden = []

        self.position_relation_full = \
            {}

        Palabra.palabras_dict[self.txt_lema + "-" + str(self.position_doc)] = self
        Palabra.relaciones_dict_origen[self] = []
        Palabra.relaciones_dict_destino[self] = []

    # get palabra by lema si existe
    @classmethod
    def get_palabra_by_lema(cls, txt_lema, position_doc):
        if Palabra.palabras_dict.get(txt_lema, None) is not None and Palabra.palabras_dict[
            txt_lema].position_doc == position_doc:
            return Palabra.palabras_dict[txt_lema]
        else:
            return None

    @classmethod
    def generar_id(cls, texto, autoincremental=True):
        if autoincremental:
            cls.id_actual += 1
            return cls.id_actual
        else:
            texto_limpio = cls.limpiar_texto(texto)
            return hash(texto_limpio)

    @classmethod
    def reordenar_importancia_list(cls, lista):
        return sorted(lista, key=lambda x: x.importancia, reverse=False)

    @staticmethod
    def limpiar_texto(texto):
        texto_limpio = texto.lower()
        texto_limpio = re.sub(r'\W+', '', texto_limpio)
        return texto_limpio

    @staticmethod
    def get_dimension(texto):
        # Método que calcula la dimensión dependiendo del tamaño de la palabra
        return len(texto) - len(texto) // 4

    def __str__(self):
        return self.texto

    def change_lema(self, new_txt_lema):
        del Palabra.palabras_dict[self.txt_lema + "-" + str(self.position_doc)]
        self.txt_lema = new_txt_lema
        Palabra.palabras_dict[new_txt_lema + "-" + str(self.position_doc)] = self

    def delete_palabra(self):
        del Palabra.palabras_dict[self.txt_lema + "-" + str(self.position_doc)]
        del Palabra.relaciones_dict_origen[self]
        del Palabra.relaciones_dict_destino[self]

    @staticmethod
    def refresh_dict_palabras():
        # eliminar duplicados y relaciones de palabras que no tengan posicion
        for key in Palabra.relaciones_dict_destino.keys():
            values = Palabra.relaciones_dict_destino[key].copy()
            for rel in values:
                if rel.position_doc == '':
                    rel.delete_relation()

    def append_enumeracion(self, new_texto):
        if not self.is_enumeracion:
            self.list_texto_enumeracion.append(self.texto)
        self.list_texto_enumeracion.append(new_texto)
        self.is_enumeracion = True
        self.dimension_y = len(self.list_texto_enumeracion) * 3 + 2

    @staticmethod
    def _get_dim_relation_tree(relation):
        try:
            return relation.pal_dest.grafos_aproximados[0]  # cogemos el grafo mayor, que es la 1a posicion
        except Exception as _:
            return 0

    def refresh_grafos_aproximados(self):
        try:
            self.grafos_aproximados = []
            lista_relaciones_directas = Palabra.relaciones_dict_origen[self]
            self.numero_grafos = len(lista_relaciones_directas)
            for rel in lista_relaciones_directas:
                self.grafos_aproximados.append(self._get_dim_relation_tree(rel) + 1)  # +1 porque es la relacion actual
            # ordenar de mayor a menor
            self.grafos_aproximados = sorted(self.grafos_aproximados, key=lambda x: x, reverse=True)
        except Exception as _:
            pass

    def to_create_Palabra_str(self):
        return "list_palabras.append(Palabra('" + self.texto + "', '" + self.tipo + "', '" + self.lugar_sintactico + "', " + str(
            self.id) + ", " + str(self.importancia) + ", " + str(
            self.num_relaciones) + ", False, '" + self.txt_lema + "', " + str(self.position_doc) + "))"
