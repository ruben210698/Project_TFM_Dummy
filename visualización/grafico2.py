import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, RegularPolygon

# Función para dibujar aristas con flechas
def draw_edge(ax, u, v, width=1.0, color='k'):
    arrow = FancyArrowPatch(u, v, arrowstyle='->', mutation_scale=20, linewidth=width, color=color)
    ax.add_patch(arrow)

# Crear un grafo dirigido
G = nx.DiGraph()

# Añadir nodos y aristas
G.add_edge("Ruben", "come")
G.add_edge("come", "pescado")
G.add_edge("pescado", "en restaurante")

# Crear posiciones de nodos
pos = {"Ruben": (0, 0), "come": (1, 0), "pescado": (2, 0), "en restaurante": (2, -1)}

fig, ax = plt.subplots(figsize=(10, 5))

# Dibujar nodos
for node, (x, y) in pos.items():
    if node in {"Ruben", "pescado"}:
        circle = Circle((x, y), radius=0.1, color="blue", zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)
    elif node == "en restaurante":
        polygon = RegularPolygon((x, y), numVertices=4, radius=0.2, orientation=0, color="green", zorder=2)
        ax.add_patch(polygon)
        ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)

# Dibujar aristas
for edge in G.edges:
    u, v = edge
    draw_edge(ax, pos[u], pos[v], color='blue')

# Configurar límites y aspecto del gráfico
ax.set_xlim(-1, 3)
ax.set_ylim(-2, 1)
ax.set_aspect('equal')
ax.axis('off')

plt.show()
