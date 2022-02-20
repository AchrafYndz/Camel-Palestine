import pygame
from settings import screen_width, screen_height

class UI:
    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load("../assets/graphics/ui/health_bar.png").convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins
        self.coin = pygame.image.load("../assets/graphics/ui/coin.png").convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(220, 28))
        self.font = pygame.font.Font("../assets/graphics/ui/Khodijah Free.ttf", 25)

        # water
        self.water_bar = pygame.image.load("../assets/graphics/ui/water_bar.png").convert_alpha()
        self.water_bar_topleft = (54, 79)
        self.water_bar_max_width = 152
        self.water_bar_height = 4

    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect((self.health_bar_topleft), (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, "#dc4949", health_bar_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render("x " + str(amount), True, (0, 0, 0))
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)

    def show_water(self, current, full):
        self.display_surface.blit(self.water_bar, (20, 50))
        current_water_ratio = current / full
        current_bar_wid = self.water_bar_max_width * current_water_ratio
        water_bar_rect = pygame.Rect((self.water_bar_topleft), (current_bar_wid, self.water_bar_height))
        pygame.draw.rect(self.display_surface, "light blue", water_bar_rect)

    def low_water_warning(self):
        font = pygame.font.Font("../assets/graphics/ui/Khodijah Free.ttf", 50)
        text = font.render("Low water level!", True, (0, 49, 69))
        self.display_surface.blit(text, (screen_width // 6*5 - text.get_width() //2, text.get_height()/2 -5))

    def zero_health(self):
        font = pygame.font.Font("../assets/graphics/ui/Khodijah Free.ttf", 60)
        text = font.render("You died", True, (200, 49, 0))
        self.display_surface.fill("black")
        self.display_surface.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + text.get_height() // 2))
