import pygame
from sokoban import Sokoban
from tree import bfs, dfs

basic_grid = """
#######
#    @#
# . $ #
#     #
#######
    
"""

def equal_nodes(state_1, state_2):
    return (state_1.grid == state_2.grid).all()


# Calcular la distancia Manhattan
def manhattan_distance(box,goal):
    
    f_box,c_box = box
    f_goal,c_goal = goal
    
    distance = abs(f_box-f_goal) + abs(c_box-c_goal)
    
    return distance
    
# Heuristica que recibe un estado y devuelve un número
def heuristic(state):
    return sum(min(manhattan_distance(box, goal) for goal in state.goals) for box in state.boxes)


# Crear objeto Sokoban y cargar el nivel
juego = Sokoban()
juego.parse_grid(basic_grid)
root = juego
root.movements = ""
queue = [root]
visited_nodes = []


heuristic_order = []  # Valor de la Heuristica por nodo
nivel_ref = 0; # Nivel de referencia dentro de la busqueda
niveles_capa = [] # Arreglo de nivel

while queue: 

      # print("heuristic values---------")
      for obj_queue in queue:
          # print("Euristica {}   Posicion {} niveles {}".format(heuristic(obj_queue),obj_queue.player,len(obj_queue.movements)))
          niveles_capa.append(len(obj_queue.movements)) # Guardo los niveles de cada uno de los estados almacenados
          heuristic_order.append(heuristic(obj_queue)) # Guardo el valor de sus respectivasd heuristicas
         
      
      if all(nv == nivel_ref for nv in niveles_capa): # Si estoy en un nivel entero entonces voy a buscar por el orden de la Heuristica
         orden_dict = {Sokoban: heuristic_order[i] for i, Sokoban in enumerate(queue)}
         queue = sorted(queue, key = lambda s: orden_dict[s]) # Ordeno la pila
         nivel_ref +=1
         # print("Ordenado")

      heuristic_order = []       
      niveles_capa = []    
      
      current = queue.pop(0) # Extraigo el de menor Heuristica
      # print(current.player)
      visited_nodes.append(current)
      print("explorando nivel {}\t movimiento:{} \t valor Heuristica {}".format(len(current.movements), current.movements,heuristic(current)))
      if current.is_finished():
          print("Found solution")
          break
       
          
      for move in current.get_possible_moves():
          new_state = move()
          if not new_state: continue
          if new_state.is_deadlocked(): continue
          was_visited = any([equal_nodes(new_state, prev_state) for prev_state in visited_nodes])
          if was_visited: continue
          
          # print(new_state.player)
          queue.append(new_state)       
         

