from src.sokoban import Sokoban

basic_grid = """
#######
#@    #
#     #
#     #
#     #
#######
"""

def test_movements():
   s = Sokoban(basic_grid)
   assert s.player == (2, 1)
   assert s.move_up() == False
   assert s.move_left() == False
   assert s.move_right() == True
   assert s.move_down() == True
   assert s.player == (3, 2)


basic_grid_with_boxes = """
#######
#@$   #
# $   #
#     #
#     #
#######
"""

def test_boxes():
   s = Sokoban(basic_grid_with_boxes)
   assert s.player == (2, 1)
   assert s.boxes == [(2, 2), (3, 2)]
   assert s.move_right() == True
   assert s.move_down() == True
   assert s.player == (3, 2)
   assert s.boxes == [(2, 3), (4, 2)]


basic_grid_with_objective = """
#######
#@$  .#
#   $ #
#   . #
#     #
#######
"""
def test_is_finished():
   s = Sokoban(basic_grid_with_objective)
   for _ in range(2):
      s.move_right()
      assert not s.is_finished()
   s.move_right()
   s.move_down()
   assert s.is_finished()


basic_grid_without_deadlock = """
#######
#@$  .#
#   $ #
#   . #
#     #
#######
"""
def test_is_not_deadlocked():
   s = Sokoban(basic_grid_without_deadlock)
   for _ in range(2):
      s.move_right()
      assert not s.is_finished()
      assert not s.is_deadlocked()
   s.move_right()
   s.move_down()
   assert s.is_finished()
   assert not s.is_deadlocked()


basic_grid_with_deadlock = """
#######
#@$   #
#     #
#     #
#     #
#######
"""
def test_is_deadlocked():
   s = Sokoban(basic_grid_with_deadlock)
   for _ in range(2):
      s.move_right()
      assert not s.is_finished()
      assert not s.is_deadlocked()
   s.move_right()
   assert s.is_deadlocked()
