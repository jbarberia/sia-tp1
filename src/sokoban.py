import numpy as np


class Sokoban:
    """
    Clase que representa el tablero del juego Sokoban como un estado.
    En caso de que se realice una modificación (movimiento), se devuelve una
    nueva instancia de la clase como si fuera un nuevo estado.
    """

    PLAYER = "@"
    BOX = "$"
    WALL = "#"
    EMPTY = " "
    GOAL = "."
    GOAL_AND_BOX = "*"

    def __init__(self):
        """Inicializa datos de la clase"""
        self.player = None
        self.boxes = []
        self.goals = []
        self.grid = np.array([])
        self.movements = ""

    def parse_grid(self, grid: str) -> np.ndarray:
        """Transforma el tableto de juego en un array de numpy

        Args:
            grid (str): tablero en formato ASCII de acuerdo a http://www.game-sokoban.com/

        Returns:
            np.ndarray: tablero de juego en formato de array de numpy
        """
        gridlines = grid.split("\n")
        rows = len(gridlines)
        cols = max([len(row) for row in gridlines])
        self.grid = np.full((rows, cols), self.EMPTY)
        for i, row in enumerate(gridlines):
            for j, cell in enumerate(row):
                if cell == self.WALL:
                    self.grid[i, j] = self.WALL
                elif cell in self.BOX:
                    self.grid[i, j] = self.BOX
                    self.boxes.append((i, j))
                elif cell == self.GOAL:
                    self.goals.append((i, j))
                elif cell == self.GOAL_AND_BOX:
                    self.grid[i, j] = self.BOX
                    self.boxes.append((i, j))
                    self.goals.append((i, j))
                elif cell == self.PLAYER:
                    self.grid[i, j] = self.PLAYER
                    self.player = (i, j)

                

    def _move(self, x: int, y: int):
        """Mueve el jugador en la dirección indicada.

        Args:
            x (int): movimiento en horizontal
            y (int): movimiento en vertical

        Returns:
            Sokoban: nueva instancia del tablero o None si el movimiento es inválido
        """
        i, j = self.player

        invalid_moves = [
            self.grid[i + x, j + y] == self.WALL,
            self.grid[i + x, j + y] == self.BOX
            and self.grid[i + 2 * x, j + 2 * y] == self.WALL,
            self.grid[i + x, j + y] == self.BOX
            and self.grid[i + 2 * x, j + 2 * y] == self.BOX,
        ]
        if any(invalid_moves):
            return

        # Crea una nueva instancia del tablero con el movimiento ejecutado
        other = Sokoban()
        other.grid = self.grid.copy()
        other.boxes = self.boxes.copy()
        other.goals = self.goals.copy()
        other.player = self.player
        other.movements = self.movements

        if other.grid[i + x, j + y] == self.BOX:
            other.grid[i + 2 * x, j + 2 * y] = self.BOX
            box_index = other.boxes.index((i + x, j + y))
            other.boxes[box_index] = (i + 2 * x, j + 2 * y)

        other.grid[i, j] = self.EMPTY
        other.grid[i + x, j + y] = self.PLAYER
        other.player = (i + x, j + y)
        return other

    def move_up(self):
        """Mueve el jugador hacia arriba y devuelve una nueva clase.
        Si es imposible realizar el movimiento, devuelve None.
        """
        other = self._move(-1, 0)
        if other:
            other.movements += "u"
        return other

    def move_down(self):
        """Mueve el jugador hacia abajo y devuelve una nueva clase.
        Si es imposible realizar el movimiento, devuelve None.
        """
        other = self._move(1, 0)
        if other:
            other.movements += "d"
        return other

    def move_left(self):
        """Mueve el jugador hacia la izquierda y devuelve una nueva clase.
        Si es imposible realizar el movimiento, devuelve None.
        """
        other = self._move(0, -1)
        if other:
            other.movements += "l"
        return other

    def move_right(self):
        """Mueve el jugador hacia la derecha y devuelve una nueva clase.
        Si es imposible realizar el movimiento, devuelve None.
        """
        other = self._move(0, 1)
        if other:
            other.movements += "r"
        return other

    def get_possible_moves(self):
        """Devuelve una lista con los posibles movimientos para cambiar a otro
        estado.

        Returns:
            list: funciones de movimiento del jugador
        """
        return [
            self.move_down,
            self.move_up,
            self.move_right,
            self.move_left,
        ]


    def is_finished(self) -> bool:
        """Verifica si el juego ha sido completado exitosamente.

        Returns:
            bool: indicador de si el juego ha sido completado exitosamente
        """
        return all([box in self.goals for box in self.boxes])


    def is_deadlocked(self) -> bool:
        """Verifica que el juego no se encuentre en un estado sin solución.
        Esto significa que la caja se queda en una esquina y no puede ser movida.

        Returns:
            bool: indicador de si el juego está en un estado sin solución
        """


        in_corner = any([self._is_in_corner(i, j) for i, j in self.boxes if (i,j) not in self.goals])
        if in_corner: return True
            
        # Caso donde los unicos movimientos llevan a un deadlock
        ########
        # #
        # #@
        # #
        ########
        for i, j in self.boxes:
            strings = self._get_possible_movements(i, j)
            next_box_move_is_deadlock = []
            for x, y in map(self._get_coord_from_str, strings):                            
                space_to_push = self.grid[i-x, j-y] == self.EMPTY
                if space_to_push:
                    next_box_move_is_deadlock.append(self._is_in_corner(i+x, j+y))            
            if all(next_box_move_is_deadlock):
                return True

        
        return False


    def _is_in_corner(self, i:int, j:int):
        """dada una posicion, indica si se encuentra en una esquina del tablero

        Args:
            i (int): posicion horizontal
            j (int): posicion vertical

        Returns:
            bool: indicacione si esta en el tablero
        """
        if self.grid[i - 1, j] == self.WALL and self.grid[i, j - 1] == self.WALL:
            return True
        if self.grid[i - 1, j] == self.WALL and self.grid[i, j + 1] == self.WALL:
            return True
        if self.grid[i + 1, j] == self.WALL and self.grid[i, j - 1] == self.WALL:
            return True
        if self.grid[i + 1, j] == self.WALL and self.grid[i, j + 1] == self.WALL:
            return True
        return False
    

    def _get_possible_movements(self, i:int, j:int):
        """devuelve un listado de posibles movimientos a realizar

        Args:
            i (int): posicion horizontal
            j (int): posicion vertical
        """
        
        movimientos = {
            (-1,  0): "u",
            ( 1,  0): "d",
            ( 0, -1): "l",
            ( 1,  1): "r",
        }

        valid_movements = []
        for (x, y), movement in movimientos.items():
            invalid_moves = [
                self.grid[i + x, j + y] == self.WALL,
                self.grid[i + x, j + y] == self.BOX and self.grid[i + 2 * x, j + 2 * y] == self.WALL,
                self.grid[i + x, j + y] == self.BOX and self.grid[i + 2 * x, j + 2 * y] == self.BOX,
            ]
            if not any(invalid_moves):
                valid_movements.append(movement)

        return valid_movements                


    def _get_coord_from_str(self, string):
        movimientos = {
            "u": (-1,  0),
            "d": ( 1,  0),
            "l": ( 0, -1),
            "r": ( 1,  1),
        }
        return movimientos[string]
