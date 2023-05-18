
from utils.Palabra import Palabra
from utils.Relacion import Relacion

from grafico14 import generate_graph

texto = ""
def test1():
    list_palabras = []
    list_relaciones= []

    list_palabras.append(Palabra('un golden retriever', 'PROPN', 'ROOT', 10, 2, 0, False, 'golden', 15))
    list_palabras.append(Palabra('Mi perro', 'NOUN', 'nsubj', 11, 1, 0, False, 'perro', 3))
    list_palabras.append(Palabra('es', 'AUX', 'cop', 12, 1009, 0, False, 'ser', 9))
    list_palabras.append(Palabra('de / años', 'NOUN', 'nmod', 13, 1040, 0, False, 'año', 40))
    list_palabras.append(Palabra('tres', 'NUM', 'nmod', 14, 1035, 0, False, 'tres', 35))
    list_palabras.append(Palabra('adora', 'VERB', 'acl', 15, 1049, 0, False, 'adorar', 49))
    list_palabras.append(Palabra('que', 'PRON', 'nsubj', 16, 1, 0, False, 'que', 45))
    list_palabras.append(Palabra('jugar', 'VERB', 'acl', 17, 1055, 0, False, 'jugar', 55))
    list_palabras.append(Palabra('con su pelota', 'NOUN', 'acl', 18, 1068, 0, False, 'pelota', 68))
    list_palabras.append(Palabra('en el parque', 'NOUN', 'acl', 19, 1081, 0, False, 'parque', 81))
    list_palabras.append(Palabra('me da', 'VERB', 'conj', 20, 1101, 0, False, 'dar', 101))
    list_palabras.append(Palabra('siempre', 'ADV', 'PAT_CCT', 21, 1090, 0, False, 'siempre', 90))
    list_palabras.append(Palabra('la bienvenida', 'NOUN', 'conj', 22, 1107, 0, False, 'bienvenida', 107))
    list_palabras.append(Palabra('moviendo', 'VERB', 'conj', 23, 1118, 0, False, 'mover', 118))
    list_palabras.append(Palabra('la cola', 'NOUN', 'conj', 24, 1130, 0, False, 'cola', 130))
    list_palabras.append(Palabra('cuando llego', 'VERB', 'PAT_CCT', 25, 1142, 0, False, 'llegar', 142))
    list_palabras.append(Palabra('a casa', 'NOUN', 'conj', 26, 1150, 0, False, 'casa', 150))

    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('perro-3') , Palabra.palabras_dict.get('golden-15'), position_doc=3 , lugar_sintactico='nsubj', importancia = 3, id=-10))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('golden-15') , Palabra.palabras_dict.get('ser-9'), position_doc=9 , lugar_sintactico='cop', importancia = 1011, id=-11))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('golden-15') , Palabra.palabras_dict.get('año-40'), position_doc=40 , lugar_sintactico='nmod', importancia = 1042, id=-12))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('año-40') , Palabra.palabras_dict.get('tres-35'), position_doc=35 , lugar_sintactico='nmod', importancia = 2075, id=-13))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('golden-15') , Palabra.palabras_dict.get('adorar-49'), position_doc=49 , lugar_sintactico='acl', importancia = 1051, id=-14))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('que-45') , Palabra.palabras_dict.get('adorar-49'), position_doc=45 , lugar_sintactico='nsubj', importancia = 1050, id=-15))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('adorar-49') , Palabra.palabras_dict.get('jugar-55'), position_doc=55 , lugar_sintactico='acl', importancia = 2104, id=-16))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('jugar-55') , Palabra.palabras_dict.get('pelota-68'), position_doc=68 , lugar_sintactico='acl', importancia = 2123, id=-17))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('jugar-55') , Palabra.palabras_dict.get('parque-81'), position_doc=81 , lugar_sintactico='acl', importancia = 2136, id=-18))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('golden-15') , Palabra.palabras_dict.get('dar-101'), position_doc=101 , lugar_sintactico='conj', importancia = 1103, id=-19))
    list_relaciones.append(Relacion('¿cuando?', Palabra.palabras_dict.get('dar-101') , Palabra.palabras_dict.get('siempre-90'), position_doc=90 , lugar_sintactico='PAT_CCT', importancia = 2191, id=-20))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('dar-101') , Palabra.palabras_dict.get('bienvenida-107'), position_doc=107 , lugar_sintactico='conj', importancia = 2208, id=-21))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('dar-101') , Palabra.palabras_dict.get('mover-118'), position_doc=118 , lugar_sintactico='conj', importancia = 2219, id=-22))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('mover-118') , Palabra.palabras_dict.get('cola-130'), position_doc=130 , lugar_sintactico='conj', importancia = 2248, id=-23))
    list_relaciones.append(Relacion('¿cuando?', Palabra.palabras_dict.get('mover-118') , Palabra.palabras_dict.get('llegar-142'), position_doc=142 , lugar_sintactico='conj', importancia = 2260, id=-24))
    list_relaciones.append(Relacion('', Palabra.palabras_dict.get('llegar-142') , Palabra.palabras_dict.get('casa-150'), position_doc=150 , lugar_sintactico='conj', importancia = 2292, id=-25))

    return list_palabras, list_relaciones





list_palabras, list_relaciones = test1()
generate_graph(texto, list_palabras, list_relaciones)


ACTIVA_WEB = False

if ACTIVA_WEB:
    ############# Web:
    from flask import Flask, send_file
    app = Flask(__name__)
    import requests
    from PIL import Image
    import io
    #######################

    @app.route("/")
    def display_graph():
        fig = generate_graph(texto, list_palabras, list_relaciones)
        fig.savefig('graph.png', bbox_inches='tight')
        return send_file('graph.png', mimetype='image/png')

    if __name__ == "__main__":
        app.run(debug=True)






#test2() # 14
#generate_graph(texto, list_palabras, list_relaciones)
#test4() # 53
#test6() # 15
#test5() # 12

#generate_graph(texto, list_palabras, list_relaciones)
#from grafico12 import print_graph
#print_graph(texto, list_palabras, list_relaciones)


