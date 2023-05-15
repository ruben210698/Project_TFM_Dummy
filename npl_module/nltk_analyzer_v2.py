import spacy
from spacy import displacy

# Cargar el modelo de español en SpaCy
nlp = spacy.load('es_core_news_sm')

# Realizar el análisis sintáctico para la oración
doc = nlp("Mientras programo, un pájaro ha saltado por el balcón y se ha comido una golondrina")

# Imprimir el árbol de dependencias sintácticas en formato de árbol
for token in doc:
    print(token.text, token.dep_, token.head.text)

def print_tree(token, level=0):
    print('\t' * level + f"{token.text} -- {token.dep_}")
    for child in token.children:
        print_tree(child, level + 1)

root = [token for token in doc if token.head == token][0]
print_tree(root)