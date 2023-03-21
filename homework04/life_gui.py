import pygame
from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.speed = speed
        self.cell_size = cell_size

        self.width = self.cell_size * life.cols
        self.height = self.cell_size * life.rows
        self.screen_size = self.width, self.height

        self.screen = pygame.display.set_mode(self.screen_size)

        super().__init__(life)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        color = (0, 255, 0)
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(
                        self.screen,
                        color,
                        pygame.Rect(self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size),
                    )

    def reverse_cell(self, pos):
        x, y = pos[1] // self.cell_size, pos[0] // self.cell_size
        self.life.curr_generation[x][y] = abs(self.life.curr_generation[x][y] - 1)

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        pause = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                elif pause and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.reverse_cell(pygame.mouse.get_pos())
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            if not pause:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((10, 10), randomize=True)
    game = GUI(life, cell_size=20, speed=2)
    game.run()
