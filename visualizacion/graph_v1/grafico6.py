import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, RegularPolygon, Ellipse
import requests
from PIL import Image
import io

# Función para dibujar aristas con flechas
def draw_edge(ax, u, v, width=1.0, color='k', label='', label_offset=(0, 0)):
    arrow = FancyArrowPatch(u, v, arrowstyle='->', mutation_scale=20, linewidth=width, color=color,  width=2.0)
    ax.add_patch(arrow)
    if label:
        x_label = (u[0] + v[0]) / 2 + label_offset[0]
        y_label = (u[1] + v[1]) / 2 + label_offset[1]
        ax.text(x_label, y_label, label, fontsize=12, ha='center', va='center', zorder=3)

# Crear un grafo dirigido
G = nx.DiGraph()

# Añadir nodos y aristas
G.add_edge("Ruben", "pescado")
G.add_edge("pescado", "en restaurante")
G.add_edge("en restaurante", "Pepe")
G.add_edge("Ruben", "Universidad Politécnica de Madrid")

# Crear posiciones de nodos
pos = {
    "Ruben": (0, 0),
    "pescado": (2, 0),
    "en restaurante": (2, -2),
    "Pepe": (3, -1),
    "Universidad Politécnica de Madrid": (-1, -2),
}

fig, ax = plt.subplots(figsize=(12, 8))

# Colores
light_blue = "#4da6ff"
green = "green"
red = "red"

# Dibujar nodos
for node, (x, y) in pos.items():

    if node in {"Ruben"}:
        ellipse_width = 0.1 * len(node) + 0.2
        ellipse_height = 0.4
        ellipse = Ellipse((x, y), width=ellipse_width, height=ellipse_height, color=light_blue, zorder=2)
        ax.add_patch(ellipse)
        ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)
    elif node == "pescado":
        response = requests.get(
            'https://upload.wikimedia.org/wikipedia/commons/e/e0/Aburabote-3D-thumb.jpg')
        img = Image.open(io.BytesIO(response.content))
        fish_image = plt.imshow(img, extent=[x - 0.5, x + 0.5, y - 0.3, y + 0.3], zorder=2)
        ax.text(x, y - 0.4, 'pescado', fontsize=12, ha='center', va='center', zorder=3)

    elif node == "en restaurante":
        polygon_radius = 0.06 * len(node)
        polygon = RegularPolygon((x, y), numVertices=4, radius=polygon_radius, orientation=0, color=green, zorder=2)
        ax.add_patch(polygon)
        ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)
    elif node in {"Pepe", "Universidad Politécnica de Madrid"}:
        ellipse_width = 0.1 * len(node) + 0.2
        ellipse_height = 0.4
        color = green if node == "Pepe" else red
        ellipse = Ellipse((x, y), width=ellipse_width, height=ellipse_height, color=color, zorder=2)
        ax.add_patch(ellipse)
        ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)

# Dibujar aristas
draw_edge(ax, pos["Ruben"], pos["pescado"], color=light_blue, label='come', label_offset=(0, 0.1))
draw_edge(ax, pos["pescado"], pos["en restaurante"], color=light_blue)
draw_edge(ax, pos["en restaurante"], pos["Pepe"], color=green)
draw_edge(ax, pos["Ruben"], pos["Universidad Politécnica de Madrid"], color=red)



# Configurar límites y aspecto del gráfico
ax.set_xlim(-3, 4)
ax.set_ylim(-4, 2)
ax.set_aspect('equal')
ax.axis('on')

plt.show()
