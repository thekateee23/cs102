import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get(self, i: int, j: int) -> bool:
        if -1 < i < self.rows and -1 < j < self.cols:
            return True
        return False

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbors = []
        x, y = cell
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i, j) != (x, y) and self.get(i, j):
                    neighbors.append(self.curr_generation[i][j])
        return neighbors

    def get_next_generation(self) -> Grid:
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                cell = (i, j)
                num_living_neighbors = sum(self.get_neighbours(cell))
                if self.curr_generation[i][j]:
                    if num_living_neighbors == 2 or num_living_neighbors == 3:
                        new_grid[i][j] = 1
                else:
                    if num_living_neighbors == 3:
                        new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations  # type: ignore

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as file:
            data = file.readlines()

        height = len(data)
        width = max(len(line) for line in data)

        grid = Grid(height, width)  # type: ignore
        for i, line in enumerate(data):
            for j, char in enumerate(line.strip()):
                grid[i][j] = int(char)

        return GameOfLife(grid)

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            # Записываем размер матрицы
            f.write(f"{self.rows},{self.cols}\n")
            # Записываем матрицу клеток
            for row in self.curr_generation:
                f.write(",".join(str(cell) for cell in row) + "\n")


if __name__ == "__main__":
    l = GameOfLife((10, 10))
    print(l.get_neighbours((0, 0)))
    print(l.get_neighbours((0, 8)))
    for i in l.curr_generation:
        print(*i)
    print()
    l.step()
    for i in l.curr_generation:
        print(*i)
