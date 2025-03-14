import numpy as np


class Sokoban:
    """
    Clase que representa el tablero del juego Sokoban.    
    """

    PLAYER = 1
    BOX = 2
    WALL = 3    
    EMPTY = 0
    

    def __init__(self, grid: str):
        """Incializa el tablero y guarda la posición del jugador, cajas y objetivos.

        Args:
            grid (str): tablero en formato ASCII de acuerdo a http://www.game-sokoban.com/
        """
        self.player = None
        self.boxes = []
        self.goals = []
        self.grid = self._parse_grid(grid)


    def _parse_grid(self, grid: str) -> np.ndarray:
        """Transforma el tableto de juego en un array de numpy

        Args:
            grid (str): tablero en formato ASCII de acuerdo a http://www.game-sokoban.com/

        Returns:
            np.ndarray: tablero de juego en formato de array de numpy
        """
        gridlines = grid.split("\n")
        rows = len(gridlines)
        cols = max([len(row) for row in gridlines])
        grid = np.zeros((rows, cols))
        for i, row in enumerate(gridlines):
            for j, cell in enumerate(row):
                if cell == "#":
                    grid[i, j] = self.WALL
                elif cell == "$":
                    grid[i, j] = self.BOX
                    self.boxes.append((i, j))
                elif cell == ".":                    
                    self.goals.append((i, j))
                elif cell == "@":
                    grid[i, j] = self.PLAYER
                    self.player = (i, j)
        return grid


    def move_left(self) -> bool:
        i, j = self.player
        invalid_moves = [
            self.grid[i, j-1] == self.WALL,
            self.grid[i, j-1] == self.BOX and self.grid[i, j-2] == self.WALL,
            self.grid[i, j-1] == self.BOX and self.grid[i, j-2] == self.BOX,
        ]
        if any(invalid_moves):
            return False
        if self.grid[i, j-1] == self.BOX:
            self.grid[i, j-2] = self.BOX

            box_index = self.boxes.index((i, j-1))
            self.boxes[box_index] = (i, j-2)


        self.grid[i, j] = self.EMPTY
        self.grid[i, j-1] = self.PLAYER
        self.player = (i, j-1)
        return True
    

    def move_right(self) -> bool:
        i, j = self.player
        invalid_moves = [
            self.grid[i, j+1] == self.WALL,
            self.grid[i, j+1] == self.BOX and self.grid[i, j+2] == self.WALL,
            self.grid[i, j+1] == self.BOX and self.grid[i, j+2] == self.BOX,
        ]
        if any(invalid_moves):
            return False
        if self.grid[i, j+1] == self.BOX:
            self.grid[i, j+2] = self.BOX

            box_index = self.boxes.index((i, j+1))
            self.boxes[box_index] = (i, j+2)

        self.grid[i, j] = self.EMPTY
        self.grid[i, j+1] = self.PLAYER
        self.player = (i, j+1)
        return True
    

    def move_up(self) -> bool:
        i, j = self.player
        invalid_moves = [
            self.grid[i-1, j] == self.WALL,
            self.grid[i-1, j] == self.BOX and self.grid[i-2, j] == self.WALL,
            self.grid[i-1, j] == self.BOX and self.grid[i-2, j] == self.BOX,
        ]
        if any(invalid_moves):
            return False
        if self.grid[i-1, j] == self.BOX:
            self.grid[i-2, j] = self.BOX

            box_index = self.boxes.index((i-1, j))
            self.boxes[box_index] = (i-2, j)


        self.grid[i, j] = self.EMPTY
        self.grid[i-1, j] = self.PLAYER
        self.player = (i-1, j)
        return True
    

    def move_down(self) -> bool:
        i, j = self.player
        invalid_moves = [
            self.grid[i+1, j] == self.WALL,
            self.grid[i+1, j] == self.BOX and self.grid[i+2, j] == self.WALL,
            self.grid[i+1, j] == self.BOX and self.grid[i+2, j] == self.BOX,
        ]
        if any(invalid_moves):
            return False
        if self.grid[i+1, j] == self.BOX:
            self.grid[i+2, j] = self.BOX

            box_index = self.boxes.index((i+1, j))
            self.boxes[box_index] = (i+2, j)

        self.grid[i, j] = self.EMPTY
        self.grid[i+1, j] = self.PLAYER
        self.player = (i+1, j)
        return True


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
        for i, j in self.boxes:
            if (i, j) in self.goals: # Evita lanzar deadlock si la caja está en un objetivo
                continue
            if self.grid[i-1, j] == self.WALL and self.grid[i, j-1] == self.WALL:
                return True
            if self.grid[i-1, j] == self.WALL and self.grid[i, j+1] == self.WALL:
                return True
            if self.grid[i+1, j] == self.WALL and self.grid[i, j-1] == self.WALL:
                return True
            if self.grid[i+1, j] == self.WALL and self.grid[i, j+1] == self.WALL:
                return True
        return False
    