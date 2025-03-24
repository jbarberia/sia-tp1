"""
Para correr esta interfaz, pasar como argumento la configuracion necesaria
que a modo de ejemplo se muestra en la carpeta config/

python src/interfaz.py config.py

"""


import pygame
import os
import sys
from sokoban import Sokoban
from tree import recorre_arbol


def cargar_configuracion():
    """Carga el archivo de configuración desde los argumentos."""
    if len(sys.argv) < 2:
        print("Uso: python src/interfaz.py config.py")
        sys.exit(1)
    configfile = sys.argv[1]
    sys.path.insert(0, os.path.dirname(configfile))
    config = __import__(os.path.basename(configfile).replace(".py", ""))
    return config


def inicializar_pygame():
    """Inicializa pygame y configura la pantalla."""
    pygame.init()
    pantalla = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Sokoban con Solución Automática')
    return pantalla


def definir_colores():
    """Define y devuelve los colores utilizados en la interfaz."""
    return {
        "fondo": (30, 30, 30), "pared": (80, 80, 80), "jugador": (0, 100, 255),
        "caja": (160, 82, 45), "objetivo": (200, 180, 0), "texto": (255, 255, 255),
        "victoria": (0, 255, 0), "derrota": (255, 255, 0), "boton": (100, 100, 255),
        "boton_texto": (255, 255, 255)
    }


def crear_botones(fuente):
    """Crea y devuelve los botones de la interfaz."""
    botones = {}
    nombres = ["BFS", "DFS", "Greedy", "A*"]
    posiciones = [10, 150, 290, 430]
    for i, nombre in enumerate(nombres):
        boton = pygame.Rect(posiciones[i], 10, 120, 30)
        texto = fuente.render(f"Resolver {nombre}", True, (255, 255, 255))
        botones[nombre.lower()] = (boton, texto)
    return botones


def dibujar_escenario(pantalla, juego, colores, botones, fuente):
    """Dibuja el escenario y los elementos del juego."""
    pantalla.fill(colores["fondo"])
    for y, fila in enumerate(juego.grid):
        for x, celda in enumerate(fila):
            rect = pygame.Rect(x*40, y*40, 40, 40)
            if celda == juego.WALL:
                pygame.draw.rect(pantalla, colores["pared"], rect)
            elif (y, x) == juego.player:
                pygame.draw.rect(pantalla, colores["jugador"], rect)
            elif (y, x) in juego.boxes:
                pygame.draw.rect(pantalla, colores["caja"], rect)
            elif (y, x) in juego.goals:
                pygame.draw.rect(pantalla, colores["objetivo"], rect)
    
    for boton, texto in botones.values():
        pygame.draw.rect(pantalla, colores["boton"], boton)
        pantalla.blit(texto, (boton.x + 10, boton.y + 5))
    
    if juego.is_finished():
        pantalla.blit(fuente.render("¡Nivel completado!", True, colores["victoria"]), (160, 240))
    if juego.is_deadlocked():
        pantalla.blit(fuente.render("El juego se ha trabado", True, colores["derrota"]), (160, 240))


def procesar_eventos(pantalla, juego, colores, botones, fuente, config):
    """Maneja eventos de entrada del usuario."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.KEYDOWN:
            direcciones = {pygame.K_LEFT: juego.move_left, pygame.K_RIGHT: juego.move_right,
                           pygame.K_UP: juego.move_up, pygame.K_DOWN: juego.move_down}
            if evento.key in direcciones:
                return direcciones[evento.key]() or juego
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for nombre, (boton, _) in botones.items():
                if boton.collidepoint(evento.pos):
                    config.algoritmo = nombre
                    solucion = recorre_arbol(juego, config)

                    movimientos = {
                        "u": lambda x: x.move_up(),
                        "d": lambda x: x.move_down(),
                        "r": lambda x: x.move_right(),
                        "l": lambda x: x.move_left(),
                    }

                    for direccion in solucion["movimientos"]:
                        juego = movimientos[direccion](juego)                        
                        dibujar_escenario(pantalla, juego, colores, botones, fuente)
                        pygame.display.flip()
                        pygame.time.delay(300)
    return juego



def main():
    config = cargar_configuracion()
    pantalla = inicializar_pygame()
    colores = definir_colores()
    fuente = pygame.font.SysFont("Arial", 16)
    botones = crear_botones(fuente)   
    juego = Sokoban()
    juego.parse_grid(config.mapa)
    
    while True:
        pantalla.fill(colores["fondo"])
        dibujar_escenario(pantalla, juego, colores, botones, fuente)
        
        pygame.display.flip()
        juego = procesar_eventos(pantalla, juego, colores, botones, fuente, config)



if __name__ == "__main__":
    main()
