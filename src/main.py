import pygame as pg
import sys
import time
import math

# global constants
WINDOW_WIDTH: int = 1920
WINDOW_HEIGHT: int = 1080
GROUND_LEVEL: int = WINDOW_HEIGHT - 320
GRASS_THICCNESS: int = 32
FPS: int = 60

class Star:
    def __init__(self, x: int, y: int):
        self.top: Vector2 = pg.Vector2(x, y)
        self.pos: Vector2 = pg.Vector2(x - 32, y)
        self.width: int = 64 
        self.height: int = 56

    def draw(self, w: pg.Surface):
        x: int = self.top.x
        y: int = self.top.y

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
        pg.draw.rect(w, "black", (self.top.x - 8, self.top.y + 22, 6, 12))
        pg.draw.rect(w, "black", (self.top.x + 2, self.top.y + 22, 6, 12))
        pg.draw.rect(w, "white", (self.top.x - 6, self.top.y + 24, 2, 4))
        pg.draw.rect(w, "white", (self.top.x + 4, self.top.y + 24, 2, 4))

class Coin:
    def __init__(self, x: int, y: int):
        self.pos: Vector2 = pg.Vector2((x, y))
        self.radius: int = 24

    def draw(self, w: pg.Surface):
        pg.draw.circle(w, "gold", (self.pos.x, self.pos.y), self.radius)
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

    def draw(self, w: pg.Surface):
        for coin in self.coins: coin.draw(w)
        for star in self.stars: star.draw(w)
        for platform in self.platforms: platform.draw(w)

class Player:
    def __init__(self):
        self.width: int = 64 
        self.height: int = 72 
        self.pos: Vector2 = pg.Vector2((100, GROUND_LEVEL - self.height))
        
        self.jumping: bool = False
        self.start_jump_time: float = 0.0
        self.jump_height: int = 128
        self.peak_jump_time: int = 0.4
        self.velocity: int = 250
        
        self.primary_color: str = "purple"
        self.secondary_color: str = "yellow"
        self.glove_color: str = "white"

    def jump(self):
        elapsed_time: float = time.time() - self.start_jump_time
        a: float = self.jump_height / (self.peak_jump_time ** 2)
        y: float = (GROUND_LEVEL - self.height) - (-a * (elapsed_time - self.peak_jump_time) ** 2 + self.jump_height)
        self.pos.y = min(y, GROUND_LEVEL - self.height)

        if self.pos.y >= GROUND_LEVEL - self.height and elapsed_time > self.peak_jump_time * 2:
            self.pos.y = GROUND_LEVEL - self.height
            self.jumping = False

    def move(self, keys, dt):
        if keys[pg.K_a] and self.pos.x > 0:
            self.pos.x -= self.velocity * dt
        elif keys[pg.K_d] and self.pos.x < WINDOW_WIDTH - self.width:
            self.pos.x += self.velocity * dt

    def draw(self, w: pg.Surface, font: pg.font.Font):
        # main body
        pg.draw.rect(w, self.secondary_color, (self.pos.x, self.pos.y, self.width, 24))
        pg.draw.rect(w, self.primary_color, (self.pos.x, self.pos.y + 24, self.width, 32))
        pg.draw.rect(w, "green4", (self.pos.x, self.pos.y + 56, self.width, 16))
        pg.draw.rect(w, self.primary_color, (self.pos.x + 8, self.pos.y, 8, 24))
        pg.draw.rect(w, self.primary_color, (self.pos.x + self.width - 16, self.pos.y, 8, 24))

        # arms
        pg.draw.rect(w, self.secondary_color, (self.pos.x - 24, self.pos.y, 24, 32))
        pg.draw.rect(w, self.secondary_color, (self.pos.x + self.width, self.pos.y, 24, 32))
        pg.draw.rect(w, self.glove_color, (self.pos.x - 24, self.pos.y + 32, 24, 16))
        pg.draw.rect(w, self.glove_color, (self.pos.x + self.width, self.pos.y + 32, 24, 16))

        # face
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
        
        # hat logo
        hat_widget = font.render("W", True, "blue", self.secondary_color)
        hat_rect = hat_widget.get_rect()
        hat_rect.center = self.pos.x + self.width / 2, self.pos.y - 42 
        window.blit(hat_widget, hat_rect)

def collision_rect_rect(obj1, obj2) -> bool:
    return not (obj1.pos.x > obj2.pos.x + obj2.width  \
                or obj1.pos.x + obj1.width < obj2.pos.x  \
                or obj1.pos.y > obj2.pos.y + obj2.height \
                or obj1.pos.y + obj1.height < obj2.pos.y)

def collision_rect_circle(obj1, obj2) -> bool:
    x: int = math.floor(obj1.pos.x)
    y: int = math.floor(obj1.pos.y)
    closest_x: int = max(obj2.pos.x, min(x, obj2.pos.x + obj2.radius * 2))
    closest_y: int = max(obj2.pos.y, min(y, obj2.pos.y + obj2.radius * 2))
    distance: float = math.sqrt((closest_x - x) ** 2 + (closest_y - y) ** 2)
    return distance <= obj2.radius

def draw_ground(w: pg.Surface):
    pg.draw.rect(w, "green", (0, GROUND_LEVEL, WINDOW_WIDTH, GRASS_THICCNESS))
    pg.draw.rect(w, "burlywood4", (0, GROUND_LEVEL + GRASS_THICCNESS, WINDOW_WIDTH, GROUND_LEVEL - GRASS_THICCNESS))

def draw_stats(w: pg.Surface, coin_count: int, star_count: int):
    coin: Coin = Coin(100, 100)
    coin_count_widget: pg.Surface = font.render(f": {coin_count}", True, "white", "aqua")
    coin_count_rect: pg.Rect = coin_count_widget.get_rect()
    coin_count_rect.center: list[int] = 150, 100
    coin.draw(w)
    w.blit(coin_count_widget, coin_count_rect)
    
    star: Star = Star(100, 145)
    star_count_widget: pg.Surface = font.render(f": {star_count}", True, "white", "aqua")
    star_count_rect: pg.Rect = star_count_widget.get_rect()
    star_count_rect.center: list[int] = 150, 180
    star.draw(w)
    w.blit(star_count_widget, star_count_rect)

def draw_time(w: pg.Surface, start_time: float):
    elapsed_time: float = str(round(time.time() - start_time, 1))
    elapsed_time_widget: pg.Surface = font.render(elapsed_time, True, "white", "aqua")
    elapsed_time_rect: pg.Rect = elapsed_time_widget.get_rect()
    elapsed_time_rect.center: list[int] = WINDOW_WIDTH - 100, 100
    w.blit(elapsed_time_widget, elapsed_time_rect)

if __name__ == "__main__":
    player: Player = Player()
    start_time: float = time.time()
    coin_count: int = 0
    star_count: int = 0
    dt: int = 0

    pg.init()
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("Wario")

    font: pg.font.Font = pg.font.Font("freesansbold.ttf", 32)
    font_small: pg.font.Font = pg.font.Font("freesansbold.ttf", 16)

    clock: pg.time.Clock = pg.time.Clock()
   
    # Level #1
    coin1: Coin = Coin(550,  700- 24)
    coin2: Coin = Coin(850, 600 - 24)
    coin3: Coin = Coin(1150, 500 - 24)
    coins: list[Coin] = [coin1, coin2, coin3]

    star: Star = Star(1350, 640)
    stars: list[Star] = [star]

    platform1: Platform = Platform(400, 700, 300, 20)
    platform2: Platform = Platform(700, 600, 300, 20)
    platform3: Platform = Platform(1000, 500, 500, 20)
    platforms: list[Platform] = [platform1, platform2, platform3]

    level: Level = Level(coins, stars, platforms)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("[INFO] you closed the window")
                sys.exit(1)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not player.jumping:
                    player.jumping = True
                    player.start_jump_time = time.time()

        window.fill("aqua")
        draw_ground(window)
        draw_stats(window, coin_count, star_count)
        draw_time(window, start_time)

        for i, coin in enumerate(coins):
            if collision_rect_circle(player, coin):
                coins.pop(i)
                coin_count += 1
        
        for i, star in enumerate(stars):
            if collision_rect_rect(player, star):
                stars.pop(i)
                star_count += 1
        
        # TODO: must be able jump onto platforms 
        if player.jumping:
            player.jump()

        player.move(pg.key.get_pressed(), dt)
            
        player.draw(window, font_small)
        level.draw(window)

        dt: float = clock.tick(FPS) / 1000

        pg.display.flip()
