def equal_nodes(state_1, state_2):
    return (state_1.grid == state_2.grid).all()




def bfs(root):
    """Recorrido del arbol de posibles estados del Sokoban a traves de
    Breadth First Search. Busqueda en el arbol primero hacía los costados.

    Solo devuelve una solución posible. No la óptima.

    Args:
        root (Sokoban): estado inicial del juego.

    Returns:
        Sokoban: estado final del juego.
    """
    root.movements = ""
    queue = [root]
    visited_nodes = []

    while queue:
        current = queue.pop(0)
        visited_nodes.append(current)
        print("explorando nivel {}\tmovimiento:{}".format(len(current.movements), current.movements))

        if current.is_finished():
            print("Found solution")
            break

        for move in current.get_possible_moves():
            new_state = move()
            
            if not new_state: continue
            if new_state.is_deadlocked(): continue
                
            was_visited = any([equal_nodes(new_state, prev_state) for prev_state in visited_nodes])
            if was_visited: continue
            
            queue.append(new_state)
                
    return current


def dfs(root):
    """Recorrido del arbol de posibles estados del Sokoban a traves de
    Depth First Search. Busqueda en el arbol primero hacía abajo.

    Solo devuelve una solución posible. No la óptima.

    Args:
        root (Sokoban): estado inicial del juego.

    Returns:
        Sokoban: estado final del juego.
    """
    root.movements = ""
    queue = [root]
    while queue:
        current = queue.pop()  # En DFS se toma el primer elemento que entro
        if current.is_finished():
            print("Found solution")
            break

        for move in current.get_possible_moves():
            new_state = move()

            if new_state and not new_state.is_deadlocked():
                queue.append(new_state)

    return current
