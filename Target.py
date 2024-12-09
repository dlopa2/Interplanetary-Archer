import pygame
from pygame import SRCALPHA

import CelestialBody
import ResourceHandling
import Projectile


class Target(CelestialBody.CelestialBody):
    def __init__(self, x, y, radius, image = None):
        super().__init__(x, y, radius, 0, image)
        self.image, _ = ResourceHandling.load_png('questiontarget.png')
        self.image = pygame.transform.scale(self.image, (radius*2,radius*2))
        self.color = (0, 0, 255)
        self.rect.center = self.position
        self.isStatic = True

    def update(self, dt, celestial_bodies):
        super().update(dt, celestial_bodies)
        collided_with_target = pygame.sprite.spritecollide(self, celestial_bodies, True, pygame.sprite.collide_circle)
        if collided_with_target:
            self.kill()
            collided_with_target[0].player.blackHoleAmmo += 3


    def draw(self, screen):
        # screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)