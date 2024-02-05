import pygame
from support import import_folder
from math import sin


def wave_value():
    value = sin(pygame.time.get_ticks())
    if value >= 0:
        return 255
    else:
        return 0


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health, change_water):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.08
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (45, self.rect.height))

        # player status
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 400
        self.hurt_time = 0

        self.jump_sound = pygame.mixer.Sound("../assets/audio/effects/jump.wav")
        self.hit_sound = pygame.mixer.Sound("../assets/audio/effects/hit.wav")

        self.change_water = change_water

    def import_character_assets(self):
        character_path = "../assets/camel/"
        self.animations = {"idle": [], "run": [], "jump": [], "fall": []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder("../assets/camel/dust_particles/run/")

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        if self.facing_right:
            self.image = animation[int(self.frame_index)]
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def run_dust_animation(self):
        if self.status == "run" and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)

            else:
                dust_particle = pygame.transform.flip(dust_particle, True, False)
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
            self.change_water(-0.1)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
            self.change_water(-0.1)
        elif keys[pygame.K_s]:
            pass
        else:
            self.direction.x = 0
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.jump()
            self.change_water(-1)
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y > 1:
            self.status = "fall"
        elif self.direction.y < 0:
            self.status = "jump"
        else:
            if self.direction.x == 0:
                self.status = "idle"
            else:
                self.status = "run"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-20)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def get_spit_on(self):

        self.change_water(10)
        self.invincible = True
        self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
