import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import es_core_news_sm
import nltk
import re

# Eliminando stopwords y masculino y femenino y signos de puntuación
#TODO, no distingue bien entre masculino y femenino
# eliminar mayusculas y minusculas.
nltk.download('stopwords')
nltk.download('wordnet')

input_texto_prueba = \
"La victoria de los francos sobre los visigodos en la batalla de Vouillé en 507, con Clodoveo I, provocó la caída " \
"del Reino Visigodo de Tolosa (Toulouse), los visigodos se trasladaron con su población a Hispania, este hecho " \
"condicionó el establecimiento definitivo de los Pirineos como frontera entre la Galia, a excepción de la " \
"Septimania, y la Hispania visigoda, así como el traslado de la capital visigoda de Tolosa a Toledo. Bajo el " \
"reinado de Atanagildo los bizantinos se instalaron en el Levante, y no fueron expulsados hasta el reinado de " \
"Suintila en 625. Durante el reinado de Leovigildo se consolida el reino visigodo al que se incorpora el reino " \
"suevo, se produjo la unificación territorial de la península ibérica, permitiéndose los matrimonios mixtos de " \
"godos con hispanorromanos, y viceversa. Con Recaredo en el III Concilio de Toledo se produjo la unificación " \
"religiosa, se abandonó el arrianismo y el reino se convirtió oficialmente al catolicismo. A partir de entonces, " \
"no hubo diferencias entre la población de la Hispania visigoda. Los Concilios de Toledo se convirtieron en el" \
" poder principal del estado visigodo, como consecuencia del debilitamiento de la monarquía. Con Recesvinto, " \
"se produjo la unidad legislativa bajo un único Código de Derecho hacia 654 promulgó el Liber Iudiciorum o " \
"Código de Recesvinto. A finales del siglo VII, las luchas internas por el poder entre la nobleza son continuas." \
" Además, la crisis social y económica, llevaron al reino visigodo a una situación límite. El rey Wamba sucesor " \
"de Recesvinto, combatía a los vascones en el norte de la Península cuando surgió una nueva rebelión en la " \
"Septimania, pero consiguió apaciguarla. Su reinado acabó por una conspiración, fue depuesto tras administrarle " \
"una bebida narcótica, quedó sin sentido, y le tonsuraron, con lo cual consiguieron que no pudiera seguir siendo " \
"rey (entre los visigodos era condición inexcusable que el monarca tuviera larga cabellera). Las contiendas se " \
"generalizaron durante los reinados de Égica y Witiza. Cuando el último rey, Rodrigo alcanzó el trono, sus rivales, " \
"los partidarios de Witiza se aliaron con el líder musulmán norteafricano Táriq Ibn Ziyad, y traicionaron al ejército " \
"de Rodrigo, pasándose los witizanos al bando musulmán, quien, tras su victoria en el año 711 en la batalla de" \
" Guadalete, inicia la invasión de la península ibérica. Entre los años 716 y 725, los musulmanes conquistan la" \
" Septimania, última provincia visigoda, poniendo fin al reino visigodo de Hispania e inaugurando el período islámico" \
" en la historia de España y Portugal. Ahora bien el dominio musulmán no logró imponerse por igual en toda la " \
"península, la historia reconoce que se creó un núcleo de resistencia2​ en Asturias, con Don Pelayo noble " \
"visigodo como líder y futuro primer rey de Asturias.3​ En torno a él se unieron parte de la nobleza visigoda " \
"y población visigoda que lograron huir hacia el norte, tras la derrota del año 711; también lo hizo la población " \
"autóctona, los astures, de origen celta, que ante la grave situación olvidaron sus antiguos enfrentamientos con " \
"los visigodos. Se iniciaba la Reconquista."


# Cargar el modelo de lenguaje en español
nlp = es_core_news_sm.load()

# Definir las stopwords
stop_words = set(stopwords.words('spanish'))

# Definir el lematizador
lemmatizer = WordNetLemmatizer()

# Cargar los documentos en una lista
documents = [input_texto_prueba]

# Preprocesar los documentos
processed_docs = []
for doc in documents:
    # Eliminar comas y puntos
    doc = re.sub(r'[^\w\s]', ' ', doc)
    # Tokenizar el documento
    tokens = word_tokenize(doc)
    # Lematizar los tokens y considerar la misma raíz para masculino y femenino
    tokens = [lemmatizer.lemmatize(token.lower(), pos='n') for token in tokens]
    tokens = [lemmatizer.lemmatize(token.lower(), pos='a') for token in tokens]
    # Eliminar stopwords
    tokens = [token for token in tokens if token not in stop_words]
    # Añadir el documento preprocesado a la lista de documentos procesados
    processed_docs.append(tokens)

# Crear un diccionario a partir de los documentos
dictionary = corpora.Dictionary(processed_docs)

# Crear un corpus a partir del diccionario
corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

# Entrenar un modelo LDA (Latent Dirichlet Allocation) con el corpus
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=3, random_state=100,
                     chunksize=100, passes=10)

# Imprimir los tópicos encontrados
for idx, topic in lda_model.print_topics(-1):
    print('Tópico: {} \nPalabras clave: {}'.format(idx+1, topic))