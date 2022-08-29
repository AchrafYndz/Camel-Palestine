import pygame
import sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):

        # game attributes
        self.level = None
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0
        self.max_water = 50
        self.current_water = 12

        # audio
        self.level_bg_music = pygame.mixer.Sound("../assets/audio/level_music.wav")
        self.overworld_bg_music = pygame.mixer.Sound("../assets/audio/overworld_music.wav")

        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = "overworld"
        self.overworld_bg_music.play(loops=-1)

        # user interface
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health, self.change_water)
        self.current_health = 100
        self.coins = 0
        self.current_water = 50
        self.status = "level"
        self.overworld_bg_music.stop()
        self.level_bg_music.play(-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = "overworld"
        self.level_bg_music.stop()
        self.overworld_bg_music.play()

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.current_health += amount

    def change_water(self, amount):
        self.current_water += amount

        if self.current_water >= 50:
            self.current_water = 50

    def check_game_over(self):
        if self.current_health <= 0 or self.current_water <=0:
            current_level = self.overworld.current_level
            self.current_health = 100
            self.current_water = 50
            self.coins = 0
            self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
            self.status = "overworld"
            self.level_bg_music.stop()
            self.overworld_bg_music.play(-1)

    def check_water_level(self):
        if self.current_water <= 10:
            self.ui.low_water_warning()

    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.ui.show_water(self.current_water, self.max_water)
            self.check_game_over()
            self.check_water_level()


pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Camel Palestine")
icon = pygame.image.load("../assets/graphics/icon/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("gray")
    game.run()

    pygame.display.update()
    clock.tick(60)
