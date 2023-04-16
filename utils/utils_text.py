import re

from utils.Palabra import Palabra
from utils.Relacion import Relacion

# aqui vienen las funciones que permiten hacer modificaciones en el texto que se consideran comunes
# Las excepciones que se han visto que se deben aplicar al texto.


def unir_2_relaciones(rel1, rel2, remove_rel2=True):
    print("Uniendo relaciones: " + rel1.texto + " y " + rel2.texto)
    if rel1.position_doc <= rel2.position_doc:
        rel1.texto = rel1.texto + " " + rel2.texto
    else:
        rel1.texto = rel2.texto + " " + rel1.texto
        rel1.position_doc = rel2.position_doc
    rel1.importancia = min(rel1.importancia, rel2.importancia)
    rel1.tam_texto = Relacion.get_tam_texto(rel1.texto)
    if remove_rel2:
        rel2.delete_relation()

def unir_list_all_relaciones(list_relaciones, list_modified = []):
    #TODO meter un filtro y si es el mismo texto que no lo una.

    # En caso de que 2 relaciones tengan el mismo origen y destino, unirlas
    list_relaciones = list(set(list_relaciones))
    list_relaciones_new = list_relaciones.copy()
    for rel in list_relaciones:
        if rel.texto == 'también de':
            print("hola, la")
        for rel2 in list_relaciones:
            if rel2.texto == 'la':
                print("hola, la")
            # and rel not in list_modified and \
            if rel2 not in list_modified and \
                rel != rel2 and rel.pal_origen == rel2.pal_origen and rel.pal_dest == rel2.pal_dest:
                print(rel2.position_doc)
                print(rel.position_doc)
                unir_2_relaciones(rel, rel2)
                list_relaciones_new.remove(rel2)
                list_modified.append(rel)
                return unir_list_all_relaciones(list_relaciones_new, list_modified)

    return list_relaciones_new


def get_relation_entre_pal(pal1, pal2):
    print("Buscando relación entre " + pal1.texto)
    if pal2.texto == 'XVI':
        print("hola")
    print("Buscando relación entre " + pal2.texto)
    # Devuelve la relación entre 2 palabras
    for rel in Palabra.relaciones_dict_destino[pal2]:
        if rel.pal_origen == pal1:
            return rel
    return None



def unir_palabras_sin_relacion(pal1, pal2, list_relaciones, list_palabras, texto_entre_palabras =""):
    # TODO que si hay alguna relacion de la palabra2, que las una.

    list_rel_pal2_palx = Palabra.relaciones_dict_origen[pal2].copy()
    list_rel_palx_pal2 = Palabra.relaciones_dict_destino[pal2].copy()

    for rel in list_rel_palx_pal2:
        if rel.pal_origen != pal1:
            rel.change_pal_dest(pal1)
        else:
            rel.delete_relation()
    for rel in list_rel_pal2_palx:
        if rel.pal_dest != pal1:
            rel.change_pal_origen(pal1)
        else:
            rel.delete_relation()

    # Unir 2 palabras en una sola
    if pal1.position_doc <= pal2.position_doc:
        pal1.texto = pal1.texto + " " + texto_entre_palabras + " " + pal2.texto
        pal1.change_lema(pal1.txt_lema + " " + texto_entre_palabras + " " + pal2.txt_lema)
    else:
        pal1.texto = pal2.texto + " " + pal1.texto
        pal1.change_lema(pal2.txt_lema + " " + texto_entre_palabras + " " + pal1.txt_lema)
        pal1.position_doc = pal2.position_doc

    pal1.importancia = min(pal1.importancia, pal2.importancia)
    pal1.dimension = Palabra.get_dimension(pal1.texto)
    pal2.delete_palabra()
    # guarda todas las relaciones menos las de la pal1 y pal2 respectivamente
    list_palabras.remove(pal2)

    return list_relaciones, list_palabras



def unir_palabras(pal1, pal2, list_relaciones, list_palabras):
    if pal2.texto == 'XVI y XVII':
        print("hola")
    basic_relation = get_relation_entre_pal(pal1, pal2)
    #TODO if basic_relation == None:

    # Primero uno todas las relaciones dest en pal1 con las dest pal2, eliminando las comunes y las que hay entre
    # las 2 palabras.
    #######
    # Recorro el bucle de las relaciones entre pal0 y pal1
    list_rel_palx_pal1 = Palabra.relaciones_dict_destino[basic_relation.pal_origen].copy()

    # Todas las relaciones se tienen que unir a la de la 1a palabra
    for rel in list_rel_palx_pal1:
        # Y a todas estas relaciones, le sumo la relacion basica, ya que voy a unir ambas palabras
        if rel.pal_origen != pal2:
            unir_2_relaciones(rel, basic_relation, remove_rel2=False)
    # Una vez ya tengo esto, ya he unido las relacines de pal0 con pal1 y pal2
    # Faltan las relaciones en las que el origen es pal1 y pal2

    list_rel_pal2_palx = Palabra.relaciones_dict_origen[basic_relation.pal_dest].copy()
    list_rel_palx_pal2 = Palabra.relaciones_dict_destino[basic_relation.pal_dest].copy()

    for rel in list_rel_palx_pal2:
        if rel.pal_origen != pal1:
            rel.change_pal_dest(pal1)
        else:
            rel.delete_relation()
    for rel in list_rel_pal2_palx:
        if rel.pal_dest != pal1:
            rel.change_pal_origen(pal1)
        else:
            rel.delete_relation()

    basic_relation.delete_relation()
    list_relaciones.remove(basic_relation)

    # Unir 2 palabras en una sola
    if pal1.position_doc <= pal2.position_doc:
        pal1.texto = pal1.texto + " " + pal2.texto
        pal1.change_lema(pal1.txt_lema + " " + pal2.txt_lema)
    else:
        pal1.texto = pal2.texto + " " + pal1.texto
        pal1.change_lema(pal2.txt_lema + " " + pal1.txt_lema)
        pal1.position_doc = pal2.position_doc

    pal1.importancia = min(pal1.importancia, pal2.importancia)
    pal1.dimension = Palabra.get_dimension(pal1.texto)
    pal2.delete_palabra()
    # guarda todas las relaciones menos las de la pal1 y pal2 respectivamente
    list_palabras.remove(pal2)

    return list_relaciones, list_palabras


def detect_numero_int(txt):
    regex = re.compile(r'^\d{1,3}(,\s*\d{1,3})*(?:\s*(y|e)\s*\d{1,3}(,\s*\d{1,3})*)*$')

    if re.search(regex, txt):
        return True
    else:
        return False


def detect_numero_romano(txt):
    # Funcion que detecta si un texto es numero
    # Acepte conjunciones entre numeros
    regex = re.compile(
        r'^M{0,9}(CM|CD|D?C{0,9})(XC|XL|L?X{0,9})(IX|IV|V?I{0,9})(\s*(,|y)\s*M{0,9}(CM|CD|D?C{0,9})(XC|XL|L?X{0,9})(IX|IV|V?I{0,9}))*$')
    # Sirve tanto para "XVI", 'XVI, XVII, XVIII', 'XVI, XVII y XVIII' ...

    if re.search(regex, txt):
        return True
    else:
        return False

# Lo mismo para meses, dias...
def unir_siglos_annos_all_list(list_palabras, list_relaciones):
    # esta funcion se debe aplicar después de unir relaciones.
    encontrado = False
    # en la lista de palabras, obtener la palabra que sea del tipo 'compound' en el lugr sintactico
     # la palabra tiene que ser del tipo sinctactico Compound
    list_palabras_copy = list_palabras.copy()
    list_relaciones_copy = list_relaciones.copy()
    patron = re.compile(".*siglo.*|.*año.*|.*año.*|.*anno.*")
    for pal in list_palabras_copy:
        if encontrado:
            continue
        if pal.lugar_sintactico == 'compound' and pal.tipo == 'NOUN' and \
                (detect_numero_romano(pal.texto) or detect_numero_int(pal.texto)):
            # Esto es el numero del siglo o del año:
            list_relaciones_posibles = Palabra.relaciones_dict_destino[pal]
            for relation in list_relaciones_posibles:
                if patron.search(relation.pal_origen.texto):
                    encontrado = True
                    # Busco todas las relaciones de la palabra origen y las junto a la de destino
                    list_relaciones, list_palabras = \
                        unir_palabras(relation.pal_origen, pal, list_relaciones, list_palabras)

                    return unir_siglos_annos_all_list(list_palabras, list_relaciones)

    return list_palabras, list_relaciones



def unir_conjuncion_y(list_palabras, list_relaciones):
    # Esto hay que hacerlo lo primero
    dict_txt_all_relations = {}
    for a in list_relaciones:
        dict_txt_all_relations.update({a: a.texto})

    dict_palabras_juntar = {}
    list_rel_y_eliminar = []

    list_palabras_copy = list_palabras.copy()
    list_relaciones_copy = list_relaciones.copy()
    for basic_rel_y in list_relaciones_copy:
        if basic_rel_y.texto == 'y' or basic_rel_y.texto == 'e' or basic_rel_y.texto == ',':
            relaciones_dict_dest_copy = Palabra.relaciones_dict_destino[basic_rel_y.pal_dest].copy()
            for rel in relaciones_dict_dest_copy:
                # si en list_relaciones hay una relacion con el mismo texto y la misma posicion pero es distinta Relacion
                # Significa que ese "y" es un complemento a otra relacion anterior.
                # Es por ello que eliminaremos esa relación.
                # una vez eliminadas todas las relaciones duplicadas, uniremos las palabras que estén relacionadas.

                dict_txt_withour_me = dict_txt_all_relations.copy()
                if rel not in dict_txt_withour_me or rel == basic_rel_y:
                    continue

                dict_txt_withour_me.pop(rel)

                # obtener indices de los valores con el mismo value que el texto
                list_indices = [i for i, x in enumerate(dict_txt_withour_me.values()) if x == rel.texto]
                list_relaciones_with_same_text = [list(dict_txt_withour_me.keys())[i] for i in list_indices]
                # obtener las relaciones con el mismo texto y la misma posicion
                list_relaciones_with_same_text_and_position = [rel2 for rel2 in list_relaciones_with_same_text if
                                                                rel2.position_doc == rel.position_doc]
                for rel2 in list_relaciones_with_same_text_and_position:
                    if rel2 != rel:# and rel.pal_dest != basic_rel_y.pal_dest:
                        # Eliminar la relacion 1, dejar solo la relacion 2 y luego unir las palabras
                        rel.delete_relation()
                        list_relaciones.remove(rel)
                        if list_rel_y_eliminar.count(basic_rel_y) == 0:
                            list_rel_y_eliminar.append(basic_rel_y)
                        dict_palabras_juntar.update({rel2.pal_dest: basic_rel_y.pal_dest})

    for rel_y in list_rel_y_eliminar:
        rel_y.delete_relation()
        list_relaciones.remove(rel_y)

    for pal1, pal2 in dict_palabras_juntar.items():
        list_relaciones, list_palabras = \
            unir_palabras_sin_relacion(pal1, pal2, list_relaciones, list_palabras, texto_entre_palabras ="y")

    return list_palabras, list_relaciones




