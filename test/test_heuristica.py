
from src.sokoban import Sokoban


basic_grid = """
#######
#    @#
# . $ #
#     #
#######    
"""

def test_distancia_manhattan():
    s = Sokoban()
    s.parse_grid(basic_grid)
    assert s.get_heuristic(["manhattan"]) == 2


def test_distancia_a_caja():
    s = Sokoban()
    s.parse_grid(basic_grid)
    assert s.get_heuristic(["distancia_a_caja"]) == 2
