import pygame as pg
import sys
import time

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
GROUND_LEVEL = WINDOW_HEIGHT / 2
FPS = 60

class Game:
    def __init__(self):
        self.start_time = time.time()
        self.elapsed_time = None

    def import_textures(self):
        pass

class Level:
    def __init__(self):
        pass

class Player:
    def __init__(self):
        self.width = 64 
        self.height = 128 
        self.color = "yellow"
        self.pos = pg.Vector2((WINDOW_WIDTH / 2 - self.width, GROUND_LEVEL - self.height))
        self.jumping = False
        self.jump_height = 128
        self.peak_jump_time = 0.5 * 1000

    def jump(self):
        a = self.jump_height / (self.peak_jump_time ** 2)
        y = (GROUND_LEVEL - self.height) - (-a * (elapsed_time - self.peak_jump_time) ** 2 + self.jump_height)
        self.pos.y = min(y, GROUND_HEIGHT - self.height)

if __name__ == "__main__":
    game = Game()
    player = Player()
    pg.init()
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("WARIO")
    clock = pg.time.Clock()
    dt = 0
    start_time = time.time()
    start_jump_time = None
    font = pg.font.Font("freesansbold.ttf", 32)

    # game-loop
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("You closed the window")
                sys.exit(1)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not player.jumping:
                    start_jump_time = time.time()

        window.fill("aqua")
        pg.draw.rect(window, "green", (0, WINDOW_HEIGHT / 2, WINDOW_WIDTH, 32))
        pg.draw.rect(window, "burlywood4", (0, GROUND_LEVEL + 32, WINDOW_WIDTH, GROUND_LEVEL - 32))

        if player.jumping:
            elapsed_jump_time = time.time() - start_jump_time
            player.jump()

        pg.draw.rect(window, player.color, (player.pos.x, player.pos.y, player.width, player.height))

        game.elapsed_time   = time.time() - game.start_time
        elapsed_time_widget = font.render(f"{round(game.elapsed_time, 1)}", True, "white", "aqua")
        elapsed_time_rect   = elapsed_time_widget.get_rect()
        elapsed_time_rect.center = WINDOW_WIDTH - 100, 100
        window.blit(elapsed_time_widget, elapsed_time_rect)
        
        pg.display.flip()
        dt = clock.tick(FPS)
