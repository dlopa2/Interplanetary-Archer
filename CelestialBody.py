import pygame
import math

from ResourceHandling import load_png


class CelestialBody(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, mass, velocity=None, image_path=None):
        super().__init__()
        self.radius = radius
        self.mass = mass
        self.isStatic = False
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0) if velocity is None else velocity
        self.moons = pygame.sprite.Group()


        #Try to load image if not use a circle
        if image_path:
            self.image, self.rect = load_png(image_path)
            self.base_image = self.image
            self.image = pygame.transform.scale(self.image, (radius*2, radius*2))
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            self.base_image = self.image
            self.rect = self.image.get_rect()
            pygame.draw.circle(self.image, (0, 255, 0), (radius, radius), radius)

    def update(self, dt, celestial_bodies, all_bodies=None):
        if self.moons:
            self.moons.update(dt, pygame.sprite.Group(self, celestial_bodies))
        self.update_static_body(dt) if self.isStatic else self.update_dynamic_body(dt, celestial_bodies)
        if all_bodies:
            self.collide_bounce(all_bodies)

    def update_static_body(self, dt):
        if self.velocity.magnitude() > 0:
            self.velocity *= 0.99
            self.position += self.velocity * dt
        self.rect.center = self.position

    def update_dynamic_body(self, dt, celestial_bodies):
        self.calculate_movement(celestial_bodies, dt)
        self.position += self.velocity * dt
        self.rect.center = self.position

    def collide_bounce(self, celestial_bodies):
        for body in celestial_bodies.sprites():
            if body != self and self.check_collision(body):
                # Calculate the normal vector
                normal = self.position - body.position
                if normal.length() != 0:
                    normal = normal.normalize()
                else:
                    return
                # Calculate the overlap distance
                overlap = self.radius + body.radius - self.position.distance_to(body.position)
                # Adjust positions to resolve overlap
                self.position += normal * (overlap / 2)
                body.position -= normal * (overlap / 2)
                # Reflect velocities
                self.velocity = self.velocity.reflect(normal)
                body.velocity = body.velocity.reflect(-normal)
    #Calculate new movement of the celestial body based by computing vector sum of all celestial bodies in a Group
    def calculate_movement(self, celestial_bodies, dt):
        acceleration = pygame.Vector2(0, 0)
        for body in celestial_bodies.sprites():
            if body != self:
                force = self.calculate_gravitational_force_vector(body)
                #a = F/m
                acceleration += force / self.mass
            #Check collision and bounce
                #self.collide_bounce(body)
        self.velocity += acceleration * dt * 100

    #Calculate the gravitational force vector between two celestial bodies
    def calculate_gravitational_force_vector(self, other):
        # Calculate the gravitational force between two celestial bodies
        # F = G * m1 * m2 / r^2
        force = 6.6743 * self.mass * other.mass / (self.position.distance_to(other.position)) ** 2
        direction = other.position - self.position
        direction.normalize_ip()
        return direction * force

    def check_collision(self, other):
        return pygame.sprite.collide_circle(self, other)

    def draw(self, screen):
        screen.blit(self.image, self.rect)