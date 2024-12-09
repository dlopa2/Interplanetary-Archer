import pygame
import math
import gui
import constants

from CelestialBody import CelestialBody
from Interplanetary_Archer.Projectile import BlackHole
from Projectile import Projectile, ScatterShot, SpaceShip
from constants import Helpers
import ResourceHandling

#types = ["Arrow","Rocket","SpaceArrow","Spaceship"]
types = ["arrow.png","rocketarrow.png","spacearrow.png","spaceship.png", "blackholeHorizon.png"]


class Player(pygame.sprite.Sprite):
    def __init__(self, col, planet, distance, angle=0, playernum = ""):
        pygame.sprite.Sprite.__init__(self)

        #inital player health and ammo
        self.health = 3
        self.scatterAmmo = 3
        self.ammo = 1
        self.blackHoleAmmo = 0
        self.arrowType = types[2]
        self.playernum = playernum

        #Player image and collision construct
        self.playerModel, self.playerModel_rect = ResourceHandling.load_png('astronaught.png')
        self.rect = self.playerModel_rect
        self.image = self.playerModel
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.playerModel, -90)
        self.mask = pygame.mask.from_surface(self.image)

        #Player aiming projectile
        self.start_projectile_pos = None
        self.launching_projectile = None
        self.projectiles = pygame.sprite.Group()

        #Initial player construction
        self.col = col
        self.planet = planet
        self.distance = distance + 22
        self.angle = angle
        self.prevAngle = -1
        self.speed = 300

        self.shot = False
        self.update_position()
        self.id = 0



    def update_position(self):
        if not (self.prevAngle == self.angle):
            self.image = pygame.transform.scale(self.playerModel, (50, 50))
            self.image = pygame.transform.rotate(self.image, -self.angle + -90)
            self.rect = self.image.get_rect(center = self.playerModel_rect.center)
            self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = self.planet.position.x + self.distance * math.cos(math.radians(self.angle))
        self.rect.centery = self.planet.position.y + self.distance * math.sin(math.radians(self.angle))
        self.prevAngle = self.angle

    def update(self, dt, celestial_bodies):
        keys = pygame.key.get_pressed()

        #Moves player counter clockwise (A)
        if keys[pygame.K_a]:
            self.angle -= self.speed * dt

        #Moves player clockwise (D)
        if keys[pygame.K_d]:
            self.angle += self.speed * dt

        #Change ammo type (1-4)
        if keys[pygame.K_1]:
            self.arrowType = types[0]
        if keys[pygame.K_2]:
            self.arrowType = types[1]
        if keys[pygame.K_3]:
            self.arrowType = types[2]
        if keys[pygame.K_4]:
            self.arrowType = types[3]
        if keys[pygame.K_5]:
            self.arrowType = types[4]

        self.update_position()
        self.projectiles.update(dt, celestial_bodies)

    def draw(self, screen, celestial_bodies):
        for projectile in self.projectiles:
            projectile.draw(screen)
        screen.blit(self.image, self.rect)
        if self.launching_projectile:
            self.draw_aiming_line(screen, celestial_bodies)

    def draw_aiming_line(self, screen, celestial_bodies):
        # Define positions using Vector2
        start_pos = pygame.Vector2(self.rect.center)
        end_pos = pygame.Vector2(pygame.mouse.get_pos())

        # Calculate angle and speed to adjust the endpoint
        angle, speed = Helpers.calculate_angle_and_speed(self.start_projectile_pos, end_pos)

        #Make length of line, last variable
        draw_speed = Helpers.map_range(speed, 0, 1200, 0, 300)
        end_pos = Helpers.calculate_point_at_angle(start_pos, -angle, draw_speed)

        # Calculate aim point
        aim_body = Projectile(end_pos.x, end_pos.y, speed, angle, 5, 0.05, None, None)
        aim_body.calculate_movement(celestial_bodies, 1)
        aim_velocity = aim_body.velocity
        angle, speed2 = Helpers.calculate_angle_and_speed((aim_velocity.x, aim_velocity.y), end_pos)
        aim_point = Helpers.calculate_point_at_angle(end_pos, -angle, 20)
        Helpers.draw_arc_between_points(screen, start_pos, end_pos, aim_point, (255, 255, 255), 5)
        #pygame.draw.lines(screen, (255, 255, 255), False, [start_pos, end_pos, aim_point], 2)

    #Returns a new Projectile object
    def shoot(self, angle, speed):
        #Normal arrow
        if self.arrowType == types[0]:
            projectile = Projectile(self.rect.centerx, self.rect.centery, speed*1.5, angle, 5, 0.05, self, self.arrowType)
        #Rocket arrow
        elif self.arrowType == types[1]:
            projectile = Projectile(self.rect.centerx, self.rect.centery, speed*3, angle, 5, 0.01, self, self.arrowType)
        #Scatter arrow
        elif self.arrowType == types[2] and self.scatterAmmo != 0:
            self.scatterAmmo -= 1
            projectile = ScatterShot(self.rect.centerx, self.rect.centery, speed*1.5, angle, 5, 0.01, self, self.arrowType)
        #Spaceship
        elif self.arrowType == types[3]:
            projectile = SpaceShip(self.rect.centerx, self.rect.centery, speed*1.5, angle, 5, 0.05, self, self.arrowType)
        #Blackhole
        elif self.arrowType == types[4] and self.blackHoleAmmo != 0:
            self.blackHoleAmmo -= 1
            projectile = BlackHole(self.rect.centerx, self.rect.centery, speed*1.5, angle, 15, 9999, self, self.arrowType)
        else:
            projectile = False
        self.shot = True
        return projectile

    def hit(self, other_player):
        for projectile in other_player.projectiles:
            projmask = pygame.mask.from_surface(projectile.image)
            hit_player = self.mask.overlap(projmask, (projectile.rect.x - self.rect.x, projectile.rect.y - self.rect.y))
            if hit_player:
                other_player.projectiles.remove(projectile)
                self.health -= 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.launching_projectile = True
            self.start_projectile_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.launching_projectile = False
            end_projectile_pos = pygame.mouse.get_pos()
            if end_projectile_pos and self.start_projectile_pos:
                angle, speed = Helpers.calculate_angle_and_speed(self.start_projectile_pos, end_projectile_pos)
                print(angle, speed * 2)
                projectile = self.shoot(-angle, speed * 2)
                if not projectile:
                    self.shot = False
                    return
                self.projectiles.add(projectile)

    def draw_gui(self, screen):
        # Draw health amount on screen
        heartImg, _ = ResourceHandling.load_png("heart.png");
        ratio = (1, 1)
        gui.draw_playernum(self.playernum, constants.WHITE, screen)
        if self.playernum == "1":
            gui.draw_text("HEALTH: ", constants.WHITE, 10, 35, screen, heartImg, self.health, self.playernum, ratio)
        elif self.playernum == "2":
            gui.draw_text("  :HEALTH", constants.WHITE, 10, 35, screen, heartImg, self.health, self.playernum, ratio)

        # Depending on ammo selected, display that type
        ammoAmt = 0
        ammoImg = None

        if self.arrowType == types[0]:
            ammoImg, _ = ResourceHandling.load_png("arrow.png")
            ammoAmt = 1
            ratio = (1,1)
        elif self.arrowType == types[1]:
            ammoImg, _ = ResourceHandling.load_png("rocketarrow.png")
            ammoAmt = 1
            ratio = (1, 1)
        elif self.arrowType == types[2]:
            ammoImg, _ = ResourceHandling.load_png("spacearrow.png")
            ammoAmt = self.scatterAmmo
            ratio = (1, 1)
        elif self.arrowType == types[3]:
            ammoImg, _ = ResourceHandling.load_png("spaceship.png")
            ammoAmt = 1
            ratio = (1, 1)
        elif self.arrowType == types[4]:
            ammoImg, _ = ResourceHandling.load_png("blackholeHorizon.png")
            ammoAmt = self.blackHoleAmmo
            ratio = (2,1)
        # Dram ammo amount on screen
        if self.playernum == "1":
            gui.draw_text("AMMO: ", constants.WHITE, 10, 105, screen, ammoImg, ammoAmt, self.playernum, ratio)
        elif self.playernum == "2":
            gui.draw_text("  :AMMO", constants.WHITE, 10, 105, screen, ammoImg, ammoAmt, self.playernum, ratio)

