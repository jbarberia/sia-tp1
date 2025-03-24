import pygame
import os
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from sokoban import Sokoban
from tree import recorre_arbol

class SokobanUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sokoban Solver UI")
        
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Cargar Config", command=self.cargar_nueva_config)
        self.file_menu.add_command(label="Reiniciar", command=self.reiniciar_juego)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=root.quit)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        
        self.algorithm_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.algorithm_menu.add_command(label="BFS", command=lambda: self.ejecutar_algoritmo("bfs"))
        self.algorithm_menu.add_command(label="DFS", command=lambda: self.ejecutar_algoritmo("dfs"))
        self.algorithm_menu.add_command(label="Greedy", command=lambda: self.ejecutar_algoritmo("greedy"))
        self.algorithm_menu.add_command(label="A*", command=lambda: self.ejecutar_algoritmo("a_star"))
        self.algorithm_menu.add_separator()
        self.algorithm_menu.add_command(label="Ejecutar todos", command=lambda: self.ejecutar_todos_algoritmos())
        self.menu_bar.add_cascade(label="Algoritmos", menu=self.algorithm_menu)

        self.resultados_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.resultados_menu.add_command(label="Mostrar resultados", command=lambda: self.mostrar_resultados())
        self.menu_bar.add_cascade(label="Resultados", menu=self.resultados_menu)

        self.embed_pygame = tk.Frame(root, width=640, height=480)
        self.embed_pygame.pack()
        self.root.bind("<KeyPress>", self.procesar_tecla)
        
        self.config = self.cargar_configuracion()
        os.environ['SDL_WINDOWID'] = str(self.embed_pygame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        
        self.pantalla = self.inicializar_pygame()
        self.colores = self.definir_colores()
        self.fuente = pygame.font.SysFont("Arial", 16)
        self.juego = Sokoban()
        self.juego.parse_grid(self.config.mapa)
        self.solucion = ""

        self.resultados = ""
        
        self.actualizar_pantalla()
    
    def cargar_configuracion(self, configfile=None):
        if configfile is None:
            configfile = os.path.join(os.path.dirname(__file__), "default_config.py")
        sys.path.insert(0, os.path.dirname(configfile))
        return __import__(os.path.basename(configfile).replace(".py", ""))
    
    def inicializar_pygame(self):
        pygame.init()
        return pygame.display.set_mode((640, 480))
    
    def definir_colores(self):
        return {"fondo": (30, 30, 30), "pared": (80, 80, 80), "jugador": (0, 100, 255),
                "caja": (160, 82, 45), "objetivo": (200, 180, 0), "texto": (255, 255, 255),
                "victoria": (0, 255, 0), "derrota": (255, 255, 0)}
    
    def actualizar_pantalla(self):
        self.pantalla.fill(self.colores["fondo"])
        for y, fila in enumerate(self.juego.grid):
            for x, celda in enumerate(fila):
                rect = pygame.Rect(x*40, y*40, 40, 40)
                if celda == self.juego.WALL:
                    pygame.draw.rect(self.pantalla, self.colores["pared"], rect)
                elif (y, x) == self.juego.player:
                    pygame.draw.rect(self.pantalla, self.colores["jugador"], rect)
                elif (y, x) in self.juego.boxes:
                    pygame.draw.rect(self.pantalla, self.colores["caja"], rect)
                elif (y, x) in self.juego.goals:
                    pygame.draw.rect(self.pantalla, self.colores["objetivo"], rect)
        
        if self.juego.is_finished():
            self.pantalla.blit(self.fuente.render("¡Nivel completado!", True, self.colores["victoria"]), (160, 240))
        
        if self.juego.is_deadlocked():
            self.pantalla.blit(self.fuente.render("¡Juego Bloqueado!", True, self.colores["derrota"]), (160, 240))

        pygame.display.flip()
        self.root.after(200, self.actualizar_pantalla)


    def procesar_tecla(self, event):
        """Procesa el evento de teclado y mueve el jugador."""
        direcciones = {
            "Up": self.juego.move_up,
            "Down": self.juego.move_down,
            "Left": self.juego.move_left,
            "Right": self.juego.move_right
        }
        if event.keysym in direcciones:
            juego = direcciones[event.keysym]()
            self.juego = juego if juego else self.juego
            self.actualizar_pantalla()
            
    
    def ejecutar_algoritmo(self, algoritmo):
        "Ejecuta el algoritmo seleccionado y luego dispara las teclas para la solución."
        self.config.algoritmo = algoritmo
        self.solucion = recorre_arbol(self.juego, self.config)

        evento = {
            "r": "<KeyPress-Right>",
            "l": "<KeyPress-Left>",
            "d": "<KeyPress-Down>",
            "u": "<KeyPress-Up>",
        }
        for direccion in self.solucion["movimientos"]:   
            self.root.event_generate(evento[direccion])
            time.sleep(0.2)

        # Guarda resultados
        solucion = self.solucion
        mensaje = ""
        mensaje += "{}\n".format(self.config.algoritmo)
        mensaje += "-"*40 + "\n"
        mensaje += "Nodos recorridos:\t\t\t{}\n".format(len(solucion["nodos_explorados"]))
        mensaje += "Profundidad máxima alcanzada:\t{}\n".format(max(len(x.movements) for x in solucion["nodos_explorados"]))
        mensaje += "Nro. de movimientos:\t\t{}\n".format(len(solucion["movimientos"]))
        mensaje += "Movimientos:\t{}\n\n".format(solucion["movimientos"])
        
        self.resultados += mensaje
        
    def ejecutar_todos_algoritmos(self):
        for algoritmo in ["bfs", "dfs", "greedy", "a_star"]:
            self.ejecutar_algoritmo(algoritmo)
            self.reiniciar_juego()
        
    def mostrar_resultados(self):
        messagebox.showinfo("Resultado", self.resultados)


    def cargar_nueva_config(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Python", "*.py")])
        if archivo:
            self.config = self.cargar_configuracion(archivo)
            self.reiniciar_juego()
    
    def reiniciar_juego(self):
        self.juego = Sokoban()
        self.juego.parse_grid(self.config.mapa)
        self.solucion = ""

        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SokobanUI(root)
    root.mainloop()
