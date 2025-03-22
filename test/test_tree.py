from src.sokoban import Sokoban
from src.tree import recorre_arbol


class Config:
    pass

basic_grid_with_objective = """
#######
#@$  .#
#   $ #
#   . #
#     #
#######
"""
def test_bfs():
    s_init = Sokoban()
    s_init.parse_grid(basic_grid_with_objective)
    
    config = Config()
    config.verbose = False
    config.algoritmo = "bfs"

    s_finished = recorre_arbol(s_init, config)["solucion"]
    assert s_finished.is_finished()
    assert s_finished.movements == "rrrd"

def test_dfs():
    s_init = Sokoban()
    s_init.parse_grid(basic_grid_with_objective)

    config = Config()
    config.verbose = False
    config.algoritmo = "dfs"

    s_finished = recorre_arbol(s_init, config)["solucion"]    
    assert s_finished.is_finished()
    #assert s_finished.movements == "rrrd"

def test_greedy():
    s_init = Sokoban()
    s_init.parse_grid(basic_grid_with_objective)

    config = Config()
    config.algoritmo = "greedy"
    config.verbose = False
    config.heuristicas = ["manhattan"]

    s_finished = recorre_arbol(s_init, config)["solucion"]    
    assert s_finished.is_finished()
    assert s_finished.movements == "rrrd"

def test_a_star():
    s_init = Sokoban()
    s_init.parse_grid(basic_grid_with_objective)

    config = Config()
    config.algoritmo = "a_star"
    config.verbose = False
    config.heuristicas = ["manhattan"]

    s_finished = recorre_arbol(s_init, config)["solucion"]    
    assert s_finished.is_finished()
    assert s_finished.movements == "rrrd"
