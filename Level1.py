import pygame
import sys
import player
import math
import mainmenu
import Projectile
import constants
from CelestialBody import CelestialBody
from ResourceHandling import load_png
#from Interplanetary_Archer.Target import Target
from constants import Width, Height
import Target

# pygame setup
pygame.init()
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
running = True

#Background
bg, _ = load_png("spacebackground.png")
bg = pygame.transform.scale(bg, (Width, Height))
bg_rect = bg.get_rect()

celestial_bodies = pygame.sprite.Group()
celestial_body = CelestialBody(Width / 2, Height / 2, 50, 99999, image_path='planet1.png')
celestial_bodies.add(celestial_body)

#Add half of player height to distance 50 + 25 (player height is 50)
player = player.Player((0, 255, 0), celestial_body, celestial_body.radius)
targets = pygame.sprite.Group()
target = Target.Target(Width / 2 + 100, Height / 2 + 100, 10)
targets.add(target)
while running:
    #delta time variable to keep track of time between frames
    dt = clock.tick(120) / 1000.0
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player.handle_event(event)

    screen.blit(bg, bg_rect)

    celestial_bodies.update(dt, player.projectiles)
    targets.update(dt, player.projectiles)
    player.update(dt, celestial_bodies)

    player.draw(screen)
    celestial_bodies.draw(screen)
    targets.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()