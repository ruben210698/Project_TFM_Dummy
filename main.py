import nltk

nltk.download('punkt')

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

output = \
"La victoria de los francos sobre los visigodos en la batalla de Vouillé en 507, con Clodoveo I, provocó la caída " \
"del Reino Visigodo de Tolosa (Toulouse), los visigodos se trasladaron con su población a Hispania, este hecho " \
"condicionó el establecimiento definitivo de los Pirineos como frontera entre la Galia, a excepción de la Septimania," \
" y la Hispania visigoda, así como el traslado de la capital visigoda de Tolosa a Toledo. Ahora bien el dominio " \
"musulmán no logró imponerse por igual en toda la península, la historia reconoce que se creó un núcleo de " \
"resistencia2​ en Asturias, con Don Pelayo noble visigodo como líder y futuro primer rey de Asturias.3​ " \
"En torno a él se unieron parte de la nobleza visigoda y población visigoda que lograron huir hacia el norte," \
" tras la derrota del año 711; también lo hizo la población autóctona, los astures, de origen celta, que ante " \
"la grave situación olvidaron sus antiguos enfrentamientos con los visigodos."

#####################################################################################################################
################################### Resumen Automático ########################################################
#####################################################################################################################
def resumen_autom():
    # Tokenizar el texto en oraciones:
    oraciones = nltk.sent_tokenize(input_texto_prueba)

    # Calcular el puntaje de cada oración utilizando el algoritmo de PageRank:
    puntajes = {}
    for oracion in oraciones:
        for palabra in nltk.word_tokenize(oracion.lower()):
            if palabra.isalnum():
                if palabra not in puntajes:
                    puntajes[palabra] = 0
                puntajes[palabra] += 1
    for oracion in oraciones:
        puntaje = 0
        for palabra in nltk.word_tokenize(oracion.lower()):
            if palabra.isalnum():
                puntaje += puntajes[palabra]
        puntajes[oracion] = puntaje

    # Seleccionar las oraciones con los puntajes más altos:
    num_oraciones_resumen = 2
    oraciones_resumen = sorted(puntajes, key=puntajes.get, reverse=True)[:num_oraciones_resumen]

    # Unir las oraciones seleccionadas para crear el resumen final:

    resumen = ' '.join(oraciones_resumen)
    print(resumen)

#####################################################################################################################
################################### Enriquecimiento de texto ########################################################
#####################################################################################################################
def enriquecim_text():
    import spacy

    # Carga el modelo de lenguaje en español de spaCy
    # python -m spacy download es_core_news_sm
    nlp = spacy.load('es_core_news_sm')

    # Parsea el texto usando el modelo de lenguaje de spaCy
    doc = nlp(input_texto_prueba)

    # Itera a través de cada oración en el texto
    for oracion in doc.sents:
        # Encuentra el predicado de la oración
        predicado = None
        for token in oracion:
            if token.dep_ == 'ROOT':
                predicado = token
                break
        # Si no se puede encontrar un predicado, pasa a la siguiente oración
        if predicado is None:
            continue
        # Verifica si el predicado tiene un sujeto
        sujeto = None
        for hijo in predicado.children:
            if hijo.dep_ == 'nsubj':
                sujeto = hijo
                break
        # Si el predicado no tiene un sujeto explícito, agrega un sujeto
        if sujeto is None:
            for hijo in predicado.children:
                if hijo.pos_ == 'VERB':
                    sujeto = oracion[0:hijo.i]
                    break
            if sujeto is not None:
                sujeto = sujeto.text.strip() + ' '
                oracion.text = sujeto + oracion.text
    # Une las oraciones en un solo texto y devuelve el resultado
    return ' '.join([oracion.text for oracion in doc.sents])





print(enriquecim_text())