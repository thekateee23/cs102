import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife, speed: float) -> None:
        super().__init__(life)
        self.speed = speed

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.clear()
        screen.addstr(0, 0, "+")
        for i in range(self.life.cols):
            screen.addstr("-")
        screen.addstr("+")
        for i in range(self.life.rows):
            screen.addstr(i + 1, 0, "|")
            screen.addstr(i + 1, self.life.cols + 1, "|")
        screen.addstr(self.life.rows + 1, 0, "+")
        for i in range(self.life.cols):
            screen.addstr("-")
        screen.addstr("+")
        screen.refresh()

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j]:
                    screen.addstr(i + 1, j + 1, "*")

    def run(self) -> None:
        screen = curses.initscr()  # type: ignore
        curses.noecho()  # type: ignore
        screen.nodelay(True)  # type: ignore
        # PUT YOUR CODE HERE
        print(2)
        pause = False
        while not self.life.is_max_generations_exceeded and self.life.is_changing:
            if not pause:
                self.draw_borders(screen)
                self.draw_grid(screen)
                self.life.step()
            c = screen.getch()
            if c == ord("p"):
                pause = not pause
            elif c == ord("e"):
                break
            time.sleep(1 / self.speed)
        curses.endwin()  # type: ignore


if __name__ == "__main__":
    l = GameOfLife((3, 3))
    a = Console(l, 1.5)
    print(1)
    a.run()
