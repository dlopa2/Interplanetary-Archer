from math import atan2

import pygame
import math

from typing_extensions import override
#from sympy.physics.units import velocity

import ResourceHandling

from CelestialBody import CelestialBody
from ResourceHandling import load_png


class Projectile(CelestialBody):
    def __init__(self, x, y, speed, angle, radius, mass, player, projectile_image, velocity = None):
        super().__init__(x, y, radius, mass, image_path=projectile_image)
        self.velocity = velocity if velocity else pygame.Vector2(speed * math.cos(math.radians(angle)),
                                                                 speed * math.sin(math.radians(angle)))
        self.player = player
        self.projectile_image = projectile_image


    @override
    def update(self, dt, celestial_bodies):
        super().update(dt, celestial_bodies)
        collided_dict = pygame.sprite.groupcollide(pygame.sprite.GroupSingle(self), celestial_bodies,
                                   True, False, pygame.sprite.collide_circle)
        if len(collided_dict) > 0 and type(self) == BlackHole:
            for celestial_body in celestial_bodies.sprites():
                if len(celestial_body.moons) > 0 or celestial_body.radius >= 50:
                    celestial_body.isStatic = True
        self.image = pygame.transform.scale(self.base_image, (25, 25))

        if self.projectile_image == "spaceship.png":
            self.image = pygame.transform.scale(self.base_image, (50, 50))
        elif self.projectile_image == "blackholeHorizon.png":
            self.image = pygame.transform.scale(self.base_image, (100, 50))
        else:
            self.image = pygame.transform.scale(self.base_image, (25, 25))

        self.image = pygame.transform.rotate(self.image, math.atan2(self.velocity.y, -self.velocity.x) * (180 / math.pi) + 90)

class ScatterShot(Projectile):
    def __init__(self, x, y, speed, angle, radius, mass, player, projectile_image=None):
        super().__init__(x, y, speed, angle, radius, mass, player, projectile_image)
        self.creation_time = pygame.time.get_ticks()

    def scatterProj(self):
        angless = [275, 0, -275]
        for angle in angless:
            newVelocity = pygame.Vector2(self.velocity.x, self.velocity.y + angle)
            scatterr = Projectile(self.position.x, self.position.y, 0, 0, 5, 0.01, self.player, "spacearrow.png", newVelocity)
            self.player.projectiles.add(scatterr)

    @override
    def update(self, dt, celestial_bodies):
        super().update(dt, celestial_bodies)
        if pygame.time.get_ticks() - self.creation_time > 500:
            self.scatterProj()
            self.player.projectiles.remove(self)
            return

class SpaceShip(Projectile):
    def __init__(self, x, y, speed, angle, radius, mass, player, projectile_image=None):
        super().__init__(x, y, speed, angle, radius, mass, player, projectile_image)

    @override
    def update(self, dt, celestial_bodies):
        super().update(dt, celestial_bodies)
        rocket = pygame.sprite.Group()
        rocket.add(self)
        hit_planet = pygame.sprite.spritecollide(self, celestial_bodies, False, pygame.sprite.collide_circle)
        if hit_planet:
            self.player.planet = hit_planet[0]
            self.player.distance = self.player.planet.radius + 22

class BlackHole(Projectile):
    def __init__(self, x, y, speed, angle, radius, mass, player, projectile_image=None):
        super().__init__(x, y, speed*0.6, angle, radius, mass, player, projectile_image)
        self.creation_time = pygame.time.get_ticks()
    @override
    def update(self, dt, celestial_bodies):
        for celestial_body in celestial_bodies.sprites():
            if celestial_body.isStatic:
                celestial_body.isStatic = False
        super().update(dt, celestial_bodies)

        if pygame.time.get_ticks() - self.creation_time > 3000:
            for celestial_body in celestial_bodies.sprites():
                if len(celestial_body.moons) > 0 or celestial_body.radius >= 50:
                    celestial_body.isStatic = True
            self.player.projectiles.remove(self)
            return