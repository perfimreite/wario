import pygame as pg
import sys
import time
from pygame.surface import Surface

WINDOW_WIDTH: int = 1920
WINDOW_HEIGHT: int = 1080
GROUND_LEVEL: int = WINDOW_HEIGHT - 320
GRASS_THICCNESS: int = 32
FPS: int = 60

class Star:
    def __init__(self, x: int, y: int):
        self.pos: VECTOR2 = pg.Vector2(x, y)

    def draw(self, w: Surface):
        x = self.pos.x
        y = self.pos.y

        a: Vector2 = pg.Vector2((x, y))
        b: Vector2 = pg.Vector2((x + 12, y + 20))
        c: Vector2 = pg.Vector2((x + 32, y + 20))
        d: Vector2 = pg.Vector2((x + 16, y + 36))
        e: Vector2 = pg.Vector2((x + 22, y + 56))
        f: Vector2 = pg.Vector2((x, y + 42))
        g: Vector2 = pg.Vector2((x - 22, y + 56))
        h: Vector2 = pg.Vector2((x - 16, y + 36))
        i: Vector2 = pg.Vector2((x - 32, y + 20))
        j: Vector2 = pg.Vector2((x - 12, y + 20))

        pg.draw.polygon(w, "yellow", (a, b, c, d, e, f, g, h, i, j))
        pg.draw.rect(w, "black", (self.pos.x - 8, self.pos.y + 22, 6, 12))
        pg.draw.rect(w, "black", (self.pos.x + 2, self.pos.y + 22, 6, 12))
        pg.draw.rect(w, "white", (self.pos.x - 6, self.pos.y + 24, 2, 4))
        pg.draw.rect(w, "white", (self.pos.x + 4, self.pos.y + 24, 2, 4))

class Coin:
    def __init__(self, x: int, y: int):
        self.pos: Vector2 = pg.Vector2((x, y))

    def draw(self, w: Surface):
        pg.draw.circle(w, "gold", (self.pos.x, self.pos.y), 24)
        pg.draw.circle(w, "yellow", (self.pos.x, self.pos.y), 16)
        pg.draw.rect(w, "gold2", (self.pos.x -4, self.pos.y - 12, 8, 24))

class Platform:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.color: str = "gray"
        self.pos: Vector2 = pg.Vector2(x, y)
        self.width: int = width
        self.height: int = height

    def draw(self, w):
        pg.draw.rect(w, self.color, (self.pos.x, self.pos.y, self.width, self.height))

class Level:
    def __init__(self, coins: list[Coin], stars: list[Star], platforms: list[Platform]):
        self.coins: list[Coin] = coins 
        self.stars: list[Star] = stars 
        self.platforms: list[Platform] = platforms

    def draw(self, w: Surface):
        for c in self.coins:
            c.draw(w)
        for s in self.stars:
            s.draw(w)
        for p in self.platforms:
            p.draw(w)

class Player:
    def __init__(self):
        self.width: int = 64 
        self.height: int = 72 
        self.primary_color: str = "purple"
        self.secondary_color: str = "yellow"
        self.glove_color: str = "white"
        self.pos: Vector2 = pg.Vector2((100, GROUND_LEVEL - self.height))
        self.jumping: bool = False
        self.start_jump_time: float or None = None
        self.jump_height: int = 128
        self.peak_jump_time: int = 0.5
        self.velocity: int = 100

    def jump(self):
        elapsed_time: float = time.time() - self.start_jump_time
        a = self.jump_height / (self.peak_jump_time ** 2)
        y = (GROUND_LEVEL - self.height) - (-a * (elapsed_time - self.peak_jump_time) ** 2 + self.jump_height)
        self.pos.y = min(y, GROUND_LEVEL - self.height)

        if self.pos.y >= GROUND_LEVEL - self.height and elapsed_time > self.peak_jump_time * 2:
            self.pos.y = GROUND_LEVEL - self.height
            self.jumping = False

    def move(self, key):
        pass

    def draw(self, w: Surface, font):
        # draw main body
        pg.draw.rect(w, self.secondary_color, (self.pos.x, self.pos.y, self.width, 24))
        pg.draw.rect(w, self.primary_color, (self.pos.x, self.pos.y + 24, self.width, 32))
        pg.draw.rect(w, "green4", (self.pos.x, self.pos.y + 56, self.width, 16))
        pg.draw.rect(w, self.primary_color, (self.pos.x + 8, self.pos.y, 8, 24))
        pg.draw.rect(w, self.primary_color, (self.pos.x + self.width - 16, self.pos.y, 8, 24))

        # draw arms
        pg.draw.rect(w, self.secondary_color, (self.pos.x - 24, self.pos.y, 24, 32))
        pg.draw.rect(w, self.secondary_color, (self.pos.x + self.width, self.pos.y, 24, 32))
        pg.draw.rect(w, self.glove_color, (self.pos.x - 24, self.pos.y + 32, 24, 16))
        pg.draw.rect(w, self.glove_color, (self.pos.x + self.width, self.pos.y + 32, 24, 16))

        # draw face
        pg.draw.rect(w, self.secondary_color, (self.pos.x - 4, self.pos.y - 56, self.width + 8, 24))
        pg.draw.rect(w, "antiquewhite", (self.pos.x, self.pos.y - 32, self.width, 32))
        pg.draw.circle(w, "white", (self.pos.x + 16, self.pos.y - 20), 6)
        pg.draw.circle(w, "white", (self.pos.x + self.width - 16, self.pos.y - 20), 6)
        pg.draw.circle(w, "blue", (self.pos.x + 16, self.pos.y - 20), 2)
        pg.draw.circle(w, "blue", (self.pos.x + self.width - 16, self.pos.y - 20), 2)
        pg.draw.rect(w, "black", (self.pos.x + 4, self.pos.y - 28, 20, 6))
        pg.draw.rect(w, "black", (self.pos.x + self.width - 24, self.pos.y - 28, 20, 6))
        pg.draw.rect(w, "black", (self.pos.x + 16, self.pos.y - 12, self.width - 32, 4))
        pg.draw.rect(w, "white", (self.pos.x + 22, self.pos.y - 8, self.width - 44, 4))
        pg.draw.polygon(w, "hotpink1", ((self.pos.x + self.width / 2, self.pos.y - 24), (self.pos.x + self.width - 24, self.pos.y - 12), (self.pos.x + 24, self.pos.y - 12)))
        
        # draw hat `W`
        hat_widget      = font.render("W", True, "blue", self.secondary_color)
        hat_rect        = hat_widget.get_rect()
        hat_rect.center = self.pos.x + self.width / 2, self.pos.y - 42 
        window.blit(hat_widget, hat_rect)

def collision(obj1, obj2) -> bool:
    x = math.floor(obj1.pos.x)
    y = math.floor(obj1.pos.y)
    closest_x = max(obj2.pos.x, min(x, obj2.pos.x + obj2.width))
    closest_y = max(obj2.pos.y, min(y, obj2.pos.y + obj2.height))
    distance = math.sqrt((closest_x - x) ** 2 + (closest_y - y) ** 2)
    return distance <= self.radius

def draw_ground(w: Surface):
    pg.draw.rect(w, "green", (0, GROUND_LEVEL, WINDOW_WIDTH, GRASS_THICCNESS))
    pg.draw.rect(w, "burlywood4", (0, GROUND_LEVEL + GRASS_THICCNESS, WINDOW_WIDTH, GROUND_LEVEL - GRASS_THICCNESS))

def draw_time(w: Surface, start_time: float):
    elapsed_time             = time.time() - start_time
    elapsed_time_widget      = font.render(f"{round(elapsed_time, 1)}", True, "white", "aqua")
    elapsed_time_rect        = elapsed_time_widget.get_rect()
    elapsed_time_rect.center = WINDOW_WIDTH - 100, 100
    window.blit(elapsed_time_widget, elapsed_time_rect)

if __name__ == "__main__":
    player: Player = Player()
    start_time = time.time()

    pg.init()
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("WARIO")
    font = pg.font.Font("freesansbold.ttf", 32)
    font_small = pg.font.Font("freesansbold.ttf", 16)
   
    # Level `#1`
    coin1: Coin = Coin(550,  700- 24)
    coin2: Coin = Coin(850, 600 - 24)
    coin3: Coin = Coin(1150, 500 - 24)
    coins: list[Coin] = [coin1, coin2, coin3]
    star: Star = Star(1350, 440)
    stars: list[Star] = [star]
    platform1: Platform = Platform(400, 700, 300, 20)
    platform2: Platform = Platform(700, 600, 300, 20)
    platform3: Platform = Platform(1000, 500, 500, 20)
    platforms: list[Platform] = [platform1, platform2, platform3]

    level: Level = Level(coins, stars, platforms)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("You closed the window")
                sys.exit(1)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not player.jumping:
                    player.jumping = True
                    player.start_jump_time = time.time()

        window.fill("aqua")
        draw_ground(window)
        draw_time(window, start_time)

        if player.jumping:
            player.jump()
            
        player.draw(window, font_small)
        level.draw(window)

        pg.display.flip()
