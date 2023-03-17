import spacy
import networkx as nx
import matplotlib.pyplot as plt

# Cargar modelo de Spacy en español
nlp = spacy.load('es_core_news_sm')

# Definir texto de ejemplo
text = "El perro marrón corre en el parque. La niña feliz juega con la pelota roja."

# Procesar texto con Spacy
doc = nlp(text)

# Crear grafo vacío
G = nx.DiGraph()

# Recorrer las oraciones del texto
for sent in doc.sents:
    # Crear nodo para la oración
    G.add_node(sent)

    # Recorrer las palabras de la oración
    for token in sent:
        # Crear nodo para la palabra
        G.add_node(token)

        # Crear arista entre la palabra y la oración
        G.add_edge(sent, token)

        # Si la palabra tiene un padre, crear arista entre la palabra y su padre
        if token.dep_ != 'ROOT':
            G.add_edge(token.head, token)

# Configurar la visualización
pos = nx.spring_layout(G, seed=42) # posición de los nodos
labels = {node: str(node) for node in G.nodes()} # etiquetas de los nodos

# Dibujar el grafo
nx.draw(G, pos, labels=labels, with_labels=True)

# Mostrar la visualización
plt.show()