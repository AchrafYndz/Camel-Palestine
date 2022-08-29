import math
import pygame
from tiles import AnimatedTile


class Bullets:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("../assets/graphics/llama/spit.png"), (32, 32))
        self.rect = self.image.get_rect()
        self.direction = (0, 0)
        self.speed = 10
        self.shot = False

    def update_bullet_pos(self, screen):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Llama(AnimatedTile):
    def __init__(self, size, x, y, path, time_interval, player_rect, player_sprite):
        super().__init__(size, x, y, path)
        center_x = x + size // 2
        center_y = y + size // 2
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.player_rect = player_rect
        self.player_sprite = player_sprite
        self.time_interval = time_interval
        self.bullet = Bullets()
        self.time = 0
        self.original_frames = self.frames

    def spit_animation(self):
        self.frames = [pygame.image.load("../assets/graphics/llama/shoot animation/2.png")]
        self.time = pygame.time.get_ticks()

    def spit(self):
        current_time = pygame.time.get_ticks()
        # if more than x seconds have passed
        if current_time > self.time + 10000:
            # we reset the bullet
            self.bullet.rect.x = self.rect.x
            self.bullet.rect.y = self.rect.y
            self.time = current_time
            self.bullet.shot = False
        else:
            # if we're shooting, we reset back from the shooting animation after .2 seconds
            if self.bullet.shot:
                current_time = pygame.time.get_ticks()
                if current_time > self.time + 200:
                    self.frames = self.original_frames

            # if we're not currently shooting, we shoot
            if not self.bullet.shot:
                self.spit_animation()
                current_player_x = self.player_rect.centerx
                current_player_y = self.player_rect.centery
                direction = (current_player_x - self.rect.x, current_player_y - self.rect.y)
                length = math.hypot(*direction)

                self.bullet.direction = (direction[0]/length, direction[1]/length)
                self.bullet.shot = True

    def reverse_image(self):
        if self.player_rect.x <= self.rect.x:
            self.image = pygame.transform.flip(self.image, True, False)

        elif self.player_rect.x >= self.rect.x:
            self.image = pygame.transform.flip(self.image, False, False)

    def check_bullet_collisions(self):
        bullet_collision = pygame.Rect.colliderect(self.player_rect, self.bullet.rect)

        if bullet_collision:
            self.bullet.rect.x = self.rect.x
            self.bullet.rect.y = self.rect.y
            self.bullet.shot = False
            self.player_sprite.get_damage()
            self.player_sprite.get_spit_on()

    def update(self, shift, screen, player_rect, player_sprite):
        self.player_sprite = player_sprite
        self.player_rect = player_rect
        self.check_bullet_collisions()
        self.animate()
        self.bullet.update_bullet_pos(screen)
        self.rect.x += shift
        self.bullet.rect.x += shift
        self.reverse_image()
