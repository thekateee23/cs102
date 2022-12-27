import random
from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    pos = ((-1, 0), (0, 1))
    n = random.randint(0, 1)
    pos_n = pos[n]
    if coord[0] != 1 or coord[1] != len(grid[0]) - 2:
        if coord[0] + pos_n[0] < 1 or coord[1] + pos_n[1] > len(grid[0]) - 2:
            pos_n = pos[abs(n - 1)]
        grid[coord[0] + pos_n[0]][coord[1] + pos_n[1]] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода
    for _, cell in enumerate(empty_cells):
        grid = remove_wall(grid, cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = (
            randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
        )
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))

    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == k:
                if i > 0 and grid[i - 1][j] == 0:
                    grid[i - 1][j] = k + 1
                if j > 0 and grid[i][j - 1] == 0:
                    grid[i][j - 1] = k + 1
                if i < len(grid) - 1 and grid[i + 1][j] == 0:
                    grid[i + 1][j] = k + 1
                if j < len(grid[i]) - 1 and grid[i][j + 1] == 0:
                    grid[i][j + 1] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    cell_now = exit_coord
    pos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    path = []

    while grid[cell_now[0]][cell_now[1]] != 1:
        k = int(grid[cell_now[0]][cell_now[1]])
        for i in pos:
            if (
                0 <= cell_now[0] + i[0] < len(grid)
                and 0 <= cell_now[1] + i[1] < len(grid[0])
                and type(grid[cell_now[0] + i[0]][cell_now[1] + i[1]]) is int
                and int(grid[cell_now[0] + i[0]][cell_now[1] + i[1]]) == k - 1
            ):
                path.append(cell_now)
                cell_now = (cell_now[0] + i[0], cell_now[1] + i[1])
                break
    path.append(cell_now)
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    if coord in [
        (0, 0),
        (0, len(grid[0]) - 1),
        (len(grid) - 1, len(grid[0]) - 1),
        (len(grid) - 1, 0),
    ]:
        return True
    if (coord[0] == 0 and grid[coord[0] + 1][coord[1]] != " ") or (
        coord[0] == len(grid) - 1 and grid[coord[0] - 1][coord[1]] != " "
    ):
        return True
    if (coord[1] == 0 and grid[coord[0]][coord[1] + 1] != " ") or (
        coord[1] == len(grid[0]) - 1 and grid[coord[0]][coord[1] - 1] != " "
    ):
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[
    List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, None
    for exit in exits:
        if encircled_exit(grid, exit):
            return grid, None

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if grid[i][j] == " ":
                grid[i][j] = 0

    entry = exits[0]
    exit = exits[1]
    grid[entry[0]][entry[1]] = 1
    grid[exit[0]][exit[1]] = 0
    k = 1
    while grid[exit[0]][exit[1]] == 0:
        make_step(grid, k)
        k += 1

    print(pd.DataFrame(grid))
    path = shortest_path(grid, exit)
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"

    return grid


if __name__ == "__main__":
    # print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15, True)
    # print(pd.DataFrame(GRID))
    _, PATH = solve_maze(deepcopy(GRID))
    MAZE = add_path_to_grid(GRID, PATH)
    # print(pd.DataFrame(MAZE))
