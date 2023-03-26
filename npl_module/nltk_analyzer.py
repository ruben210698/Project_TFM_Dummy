# quiero lo mismo que en el npl_analyzer pero con el nlp de nltk
#

import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('tagsets')
nltk.download('omw')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

texto = "Ruben dibuja koalas en bañador saltando entre acantilados mientras su amigo graba la escena y se rie."

# Tokenización del texto
tokens = word_tokenize(texto)

# Eliminación de stopwords
tokens = [token for token in tokens if token.lower() not in stopwords.words('spanish')]

# Creación de lista de palabras y relaciones
list_palabras = []
list_relaciones = []
for i, token in enumerate(tokens):
    tipo_morfol = nltk.pos_tag([token])[0][1]
    lema_palabra = token

    # Crear objeto Palabra y añadir a lista de palabras
    nueva_palabra = (lema_palabra, tipo_morfol, i)
    list_palabras.append(nueva_palabra)

    # Crear objeto Relacion y añadir a lista de relaciones si el token tiene padre
    padre = nltk.parse.DependencyGraph(tree_str='( )')
    padre.root = i
    if i != 0:
        for j, rel in enumerate(nltk.parse.DependencyGraph(tree_str=nltk.ne_chunk(nltk.pos_tag([token]))).to_conll(4)):
            if j != i:
                padre.add_arc(j, i, rel)

        nueva_relacion = (padre, i, list_palabras[i])
        list_relaciones.append(nueva_relacion)
