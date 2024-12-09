# Example file showing a basic pygame "game loop"
import pygame
import sys
import player
import math
import mainmenu
import Projectile
import constants
from constants import Width, Height, GRAVITY

# pygame setup
pygame.init()
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
running = True

#send user to main menu screen, will continue here after it returns
mainmenu.menu(screen)





#Create player
plr = player.Player("Crimson", Width/2, Height/2)


#array to store projectiles
projectiles = []
launchingProjectile = False
start_projectile_pos = None
end_projectile_pos = None

while running:
    #delta time variable to keep track of time between frames
    dt = clock.tick(60) / 1000.0

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            launchingProjectile = True
            start_projectile_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            launchingProjectile = False
            end_projectile_pos = pygame.mouse.get_pos()
            if start_projectile_pos and end_projectile_pos:
                #dx is the distance between the start and end x positions of the mouse
                dx = end_projectile_pos[0] - start_projectile_pos[0]
                #dy is the distance between the start and end y positions of the mouse
                dy = end_projectile_pos[1] - start_projectile_pos[1]
                #angle is the angle between the start and end positions of the mouse calculated using atan2
                #atan2(arc tangent) returns the angle in radians between the positive x-axis of the cartesian plane and the point given
                #by the coordinates (dx, dy)
                angle = -(math.degrees(math.atan2(-dy, -dx)))
                #speed is the distance between the start and end positions of the mouse
                speed = math.hypot(dx, dy) * 5
                #create a new projectile object and add it to the projectiles array
                #projectiles.append(Projectile.Projectile(start_projectile_pos[0], start_projectile_pos[1], speed, angle))
                projectiles.append(
                    Projectile.Projectile(plr.rect.x + 100, plr.rect.y + 50, speed, angle))


    # RENDER YOUR GAME HERE
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    for projectile in projectiles:
        projectile.update(dt)

    # Draw player on screen
    #pygame.draw.rect(screen, (255, 0, 255), plr.rect)
    screen.blit(plr.image, (plr.rect.x, plr.rect.y))


    # Movement for player (WASD)
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        plr.rect.x += -plr.speed
    elif key[pygame.K_d]:
        plr.rect.x += plr.speed
    if key[pygame.K_w]:
        plr.rect.y += -plr.speed
    elif key[pygame.K_s]:
        plr.rect.y += plr.speed

    # Draw aiming line
    if launchingProjectile and start_projectile_pos:
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (0, 0, 255), start_projectile_pos, current_pos, 2)

    for projectile in projectiles:
        projectile.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()