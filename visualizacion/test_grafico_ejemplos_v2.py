
from utils.Palabra import Palabra
from utils.Relacion import Relacion

from grafico14 import generate_graph

list_palabras = []
list_relaciones = []
texto = ""
def test1():

    list_palabras.append(Palabra('Austrias', 'PROPN', 'nsubj', 10, 1004, 0, False, 'Austrias', 4))
    list_palabras.append(Palabra('España', 'PROPN', 'obj', 11, 1024, 0, False, 'España', 24))
    list_palabras.append(Palabra('siglo', 'NOUN', 'obl', 12, 1037, 0, False, 'siglo', 37))
    list_palabras.append(Palabra('XVI', 'NOUN', 'compound', 13, 1043, 0, False, 'xvi', 43))
    list_palabras.append(Palabra('responsables', 'ADJ', 'obj', 14, 1048, 0, False, 'responsable', 48))
    list_palabras.append(Palabra('Inquisición', 'PROPN', 'nmod', 15, 1075, 0, False, 'Inquisición', 75))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias-4') , Palabra.palabras_dict.get('España-24'), position_doc=13 , lugar_sintactico='obj', importancia = 2028, id=-10))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias-4') , Palabra.palabras_dict.get('siglo-37'), position_doc=13 , lugar_sintactico='obl', importancia = 2041, id=-11))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias-4') , Palabra.palabras_dict.get('responsable-48'), position_doc=13 , lugar_sintactico='obj', importancia = 2052, id=-12))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('siglo-37') , Palabra.palabras_dict.get('xvi-43'), position_doc=31 , lugar_sintactico='compound', importancia = 2080, id=-13))
    list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('siglo-37') , Palabra.palabras_dict.get('xvi-43'), position_doc=34 , lugar_sintactico='compound', importancia = 2080, id=-14))
    list_relaciones.append(Relacion('también', Palabra.palabras_dict.get('responsable-48') , Palabra.palabras_dict.get('Inquisición-75'), position_doc=61 , lugar_sintactico='nmod', importancia = 2123, id=-15))
    list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('responsable-48') , Palabra.palabras_dict.get('Inquisición-75'), position_doc=69 , lugar_sintactico='nmod', importancia = 2123, id=-22))
    list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('responsable-48') , Palabra.palabras_dict.get('Inquisición-75'), position_doc=72 , lugar_sintactico='nmod', importancia = 2123, id=-23))

def test2():
    list_palabras.append(Palabra('Austrias', 'PROPN', 'nsubj', 10, 1004, 0, False, 'Austrias', 4))
    list_palabras.append(Palabra('España', 'PROPN', 'obj', 11, 1024, 0, False, 'España', 24))
    list_palabras.append(Palabra('siglo', 'NOUN', 'obl', 12, 1037, 0, False, 'siglo', 37))
    list_palabras.append(Palabra('XVI', 'NOUN', 'compound', 13, 1043, 0, False, 'xvi', 43))
    list_palabras.append(Palabra('XVII', 'NOUN', 'conj', 14, 1049, 0, False, 'xvii', 49))
    list_palabras.append(Palabra('responsables', 'ADJ', 'obj', 15, 1055, 0, False, 'responsable', 55))
    list_palabras.append(Palabra('Inquisición', 'PROPN', 'nmod', 16, 1082, 0, False, 'Inquisición', 82))
    list_palabras.append(Palabra('expulsión', 'NOUN', 'obj', 17, 1095, 0, False, 'expulsión', 95))
    list_palabras.append(Palabra('judíos', 'NOUN', 'nmod', 18, 1108, 0, False, 'judío', 108))
    list_palabras.append(Palabra('legado', 'NOUN', 'ROOT', 19, 1119, 0, False, 'legado', 119))
    list_palabras.append(Palabra('arquitectura', 'NOUN', 'appos', 20, 1127, 0, False, 'arquitectura', 127))
    list_palabras.append(Palabra('arte', 'NOUN', 'conj', 21, 1142, 0, False, 'arte', 142))
    list_palabras.append(Palabra('Madrid', 'PROPN', 'nmod', 22, 1150, 0, False, 'Madrid', 150))
    list_palabras.append(Palabra('Córdoba', 'PROPN', 'conj', 23, 1159, 0, False, 'Córdoba', 159))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias-4') , Palabra.palabras_dict.get('España-24'), position_doc=13 , lugar_sintactico='obj', importancia = 2028, id=-10))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias-4') , Palabra.palabras_dict.get('siglo-37'), position_doc=13 , lugar_sintactico='obl', importancia = 2041, id=-11))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias-4') , Palabra.palabras_dict.get('responsable-55'), position_doc=13 , lugar_sintactico='obj', importancia = 2059, id=-12))
    list_relaciones.append(Relacion('gobernaron', Palabra.palabras_dict.get('Austrias-4') , Palabra.palabras_dict.get('expulsión-95'), position_doc=13 , lugar_sintactico='obj', importancia = 2099, id=-13))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('siglo-37') , Palabra.palabras_dict.get('xvi-43'), position_doc=31 , lugar_sintactico='compound', importancia = 2080, id=-14))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('siglo-37') , Palabra.palabras_dict.get('xvii-49'), position_doc=31 , lugar_sintactico='conj', importancia = 2086, id=-15))
    list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('siglo-37') , Palabra.palabras_dict.get('xvi-43'), position_doc=34 , lugar_sintactico='compound', importancia = 2080, id=-16))
    list_relaciones.append(Relacion('el', Palabra.palabras_dict.get('siglo-37') , Palabra.palabras_dict.get('xvii-49'), position_doc=34 , lugar_sintactico='conj', importancia = 2086, id=-17))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('siglo-37') , Palabra.palabras_dict.get('xvii-49'), position_doc=47 , lugar_sintactico='conj', importancia = 2086, id=-18))
    list_relaciones.append(Relacion('también', Palabra.palabras_dict.get('responsable-55') , Palabra.palabras_dict.get('Inquisición-82'), position_doc=68 , lugar_sintactico='nmod', importancia = 2137, id=-19))
    list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('expulsión-95') , Palabra.palabras_dict.get('judío-108'), position_doc=105 , lugar_sintactico='nmod', importancia = 2203, id=-20))
    list_relaciones.append(Relacion('su', Palabra.palabras_dict.get('legado-119') , Palabra.palabras_dict.get('arquitectura-127'), position_doc=116 , lugar_sintactico='appos', importancia = 2246, id=-21))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('arquitectura-127') , Palabra.palabras_dict.get('arte-142'), position_doc=140 , lugar_sintactico='conj', importancia = 2269, id=-22))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('arquitectura-127') , Palabra.palabras_dict.get('Madrid-150'), position_doc=147 , lugar_sintactico='nmod', importancia = 2277, id=-23))
    list_relaciones.append(Relacion('en', Palabra.palabras_dict.get('arquitectura-127') , Palabra.palabras_dict.get('Córdoba-159'), position_doc=147 , lugar_sintactico='conj', importancia = 2286, id=-24))
    list_relaciones.append(Relacion('y', Palabra.palabras_dict.get('Madrid-150') , Palabra.palabras_dict.get('Córdoba-159'), position_doc=157 , lugar_sintactico='conj', importancia = 2309, id=-25))
    list_relaciones.append(Relacion('de', Palabra.palabras_dict.get('responsable-55') , Palabra.palabras_dict.get('Inquisición-82'), position_doc=76 , lugar_sintactico='nmod', importancia = 2137, id=-36))
    list_relaciones.append(Relacion('la', Palabra.palabras_dict.get('responsable-55') , Palabra.palabras_dict.get('Inquisición-82'), position_doc=79 , lugar_sintactico='nmod', importancia = 2137, id=-37))



test2()


generate_graph(texto, list_palabras, list_relaciones)
#from grafico12 import print_graph
#print_graph(texto, list_palabras, list_relaciones)


