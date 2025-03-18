import pygame
from sokoban import Sokoban
from tree import bfs, dfs

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Sokoban con Solución Automática')

# Fuente para leyenda
fuente = pygame.font.SysFont("Arial", 16)
fuente_grande = pygame.font.SysFont("Arial", 32)

# Colores
COLOR_FONDO = (30, 30, 30)
COLOR_CAJA = (160, 82, 45)
COLOR_OBJETIVO = (200, 180, 0)
COLOR_JUGADOR = (0, 100, 255)
COLOR_PARED = (80, 80, 80)
COLOR_TEXTO = (255, 255, 255)
COLOR_VICTORIA = (0, 255, 0)
COLOR_DERROTA = (255, 255, 0)
COLOR_BOTON = (100, 100, 255)
COLOR_BOTON_TEXTO = (255, 255, 255)

# Tamaño de bloque
TAM_BLOQUE = 40

# Escenario en formato del archivo original
basic_grid = """

########
#      #
#  .*$@#
#      #
#####  #
    ####
"""

# Crear objeto Sokoban y cargar el nivel
juego = Sokoban()
juego.parse_grid(basic_grid)

solucion = []  # Almacena los movimientos de la solución
indice_movimiento = 0  # Controla el paso a paso

# Función para dibujar el escenario
def dibujar_escenario():
    pantalla.fill(COLOR_FONDO)
    filas, columnas = juego.grid.shape
    for y in range(filas):
        for x in range(columnas):
            rect = pygame.Rect(x*TAM_BLOQUE, y*TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE)
            if juego.grid[y, x] == juego.WALL:
                pygame.draw.rect(pantalla, COLOR_PARED, rect)
            elif (y, x) == juego.player:
                pygame.draw.rect(pantalla, COLOR_JUGADOR, rect)
            elif (y, x) in juego.boxes:
                pygame.draw.rect(pantalla, COLOR_CAJA, rect)
            elif (y, x) in juego.goals:
                pygame.draw.rect(pantalla, COLOR_OBJETIVO, rect)
    
    # Dibujar botón de BFS
    boton_bfs = pygame.Rect(10, 10, 120, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_bfs)
    texto_bfs = fuente.render("Resolver BFS", True, COLOR_BOTON_TEXTO)
    pantalla.blit(texto_bfs, (20, 15))
    
    # Dibujar botón de DFS
    boton_dfs = pygame.Rect(150, 10, 120, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_dfs)
    texto_dfs = fuente.render("Resolver DFS", True, COLOR_BOTON_TEXTO)
    pantalla.blit(texto_dfs, (160, 15))
    
    # Verificación de victoria
    if juego.is_finished():
        texto_victoria = fuente_grande.render("¡Nivel completado!", True, COLOR_VICTORIA)
        pantalla.blit(texto_victoria, (ANCHO // 4, ALTO // 2))

    if juego.is_deadlocked():
        texto_derrota = fuente_grande.render("El juego se ha trabado", True, COLOR_DERROTA)
        pantalla.blit(texto_derrota, (ANCHO // 4, ALTO // 2))

    return boton_bfs, boton_dfs

# Ciclo principal
corriendo = True
while corriendo:
    pantalla.fill(COLOR_FONDO)
    boton_bfs, boton_dfs = dibujar_escenario()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif evento.type == pygame.KEYDOWN:
        
            if evento.key == pygame.K_LEFT:
                nuevo_estado = juego.move_left()
            elif evento.key == pygame.K_RIGHT:
                nuevo_estado = juego.move_right()
            elif evento.key == pygame.K_UP:
                nuevo_estado = juego.move_up()
            elif evento.key == pygame.K_DOWN:
                nuevo_estado = juego.move_down()
            
            juego = nuevo_estado if nuevo_estado else juego
            
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_bfs.collidepoint(evento.pos):
                solucion = bfs(juego).movements
                
            elif boton_dfs.collidepoint(evento.pos):
                solucion = dfs(juego).movements
                
            if not solucion:
                print("Juego Terminado")
                
    
    # Ejecutar la solución paso a paso
    if solucion:
        movimiento = solucion[0]
        solucion = solucion[1:]

        if movimiento == 'l':
            nuevo_estado = juego.move_left()
        elif movimiento == 'r':
            nuevo_estado = juego.move_right()
        elif movimiento == 'u':
            nuevo_estado = juego.move_up()
        elif movimiento == 'd':
            nuevo_estado = juego.move_down()
        indice_movimiento += 1
        pygame.time.delay(300)  # Pausa entre movimientos

        if nuevo_estado:
            juego = nuevo_estado
        else:
            juego = juego
            
    pygame.display.flip()
    pygame.time.Clock().tick(60)
