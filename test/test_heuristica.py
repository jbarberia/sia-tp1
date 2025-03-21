
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
    assert s._heuristica_mahattan() == 2
