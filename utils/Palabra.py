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

"""
¿Por qué hay un id_actual que a veces es autoincremental y a veces no?
Pues porque hay palabras como verbos, adjetivos o sustantivos que se van a repetir en la oración pero
no son lo mismo.
Sin embargo, si hay palabras iguales como nombres propios, nombres de ciudades...
De esta forma, palabras que se repiten y no queremos que sean iguales en el grafo, serán autoimcrementales
y palabras que se repitan y queramos que se relacionen, se guardarán con el id como su hash y serán iguales.
"""
class Palabra:
    id_actual = 0
    palabras_dict = {}
    relaciones_dict_origen = {}
    relaciones_dict_dest = {}

    def __init__(self, texto, tipo, lugar_sintactico, id=None, importancia=99, num_relaciones=0, autoincremental=True,
                 txt_lema=None, position_doc = 9999):
        self.texto = texto
        self.txt_lema = txt_lema if txt_lema is not None else self.limpiar_texto(texto)
        self.tipo = tipo
        self.lugar_sintactico = lugar_sintactico
        self.id = id if id is not None else self.generar_id(texto, autoincremental)
        self.importancia = importancia
        self.num_relaciones = num_relaciones
        self.dimension = self.get_dimension(texto)
        self.has_been_plotted = False
        self.position_doc = position_doc

        Palabra.palabras_dict[self.txt_lema] = self
        Palabra.relaciones_dict_origen[self] = []
        Palabra.relaciones_dict_dest[self] = []

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
        return len(texto)//3

    def __str__(self):
        return self.texto