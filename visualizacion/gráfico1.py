import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Diagrama de oración")

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.G = nx.DiGraph()

        self.dibujar_grafo()

        # Vincular el evento de la rueda del ratón
        self.canvas.get_tk_widget().bind("<MouseWheel>", self.on_mouse_wheel)

    def dibujar_grafo(self):
        self.G.clear()
        self.ax.clear()

        # Oración original: Juan come pasta en casa de Inés y luego se irán a jugar a los bolos
        # Eliminar determinantes: Juan come pasta casa Inés luego irán jugar bolos
        palabras = ["Juan", "come", "pasta", "casa", "Inés", "luego", "irán", "jugar", "bolos"]
        verbos = ["come", "irán", "jugar"]

        for palabra in palabras:
            if palabra not in verbos:
                self.G.add_node(palabra, label=palabra)

        for i in range(len(palabras) - 1):
            if palabras[i] in verbos or palabras[i+1] in verbos:
                self.G.add_edge(palabras[i], palabras[i+1], label=palabras[i] if palabras[i] in verbos else palabras[i+1])

        pos = nx.spring_layout(self.G, seed=42)
        nx.draw(self.G, pos, with_labels=False, node_size=2000, ax=self.ax)

        etiquetas_nodos = {n[0]: n[1].get('label',"") for n in self.G.nodes(data=True)}
        nx.draw_networkx_labels(self.G, pos, labels=etiquetas_nodos, ax=self.ax)

        etiquetas_aristas = {(e[0], e[1]): e[2]['label'] for e in self.G.edges(data=True)}
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=etiquetas_aristas, ax=self.ax)

        self.canvas.draw()

    def on_mouse_wheel(self, event):
        pass  # No es necesario implementar esta función para este ejemplo, pero se mantiene para seguir el formato anterior

if __name__ == '__main__':
    app = App()
    app.mainloop()
