import json

import pygame
import sys
import gui

from pygame.examples.midi import null_key

import player
import math
import mainmenu
import Projectile
import constants
from CelestialBody import CelestialBody
from ResourceHandling import load_png
# from Interplanetary_Archer.Target import Target
from constants import Width, Height, Helpers
import Target

# pygame setup
pygame.init()
screen = pygame.display.set_mode((Width, Height))
running = True
controlsOpen = False

celestial_bodies = pygame.sprite.Group()
moons = pygame.sprite.Group()
targets = pygame.sprite.Group()
all_bodies = pygame.sprite.Group()
playerTurn = 1
playerCount = 2

#Background
bg = pygame.image.load("Sprites/spacebackgroundNoPlanets.png")
bg = pygame.transform.scale(bg, (Width, Height))
bg_rect = bg.get_rect()

def reinitialize_player(player):
    player.planet = celestial_bodies.sprites()[player.id-1]
    player.distance = celestial_bodies.sprites()[player.id-1].radius + 22
    player.angle = 0
    player.health = 3
    player.blackHoleAmmo = 0
    player.scatterAmmo = 3
    player.ammo = 1
    player.prevAngle = -1
    player.projectiles.empty()
    player.image = player.playerModel

def initialize():

    level = mainmenu.menu(screen)

    # Planets and Asteroids
    f = open(level)
    level_data = json.load(f)
    f.close()

    #load in planets
    celestial_bodies.empty()
    for body in level_data["planets"]:
        newBody = CelestialBody(body["x"], body["y"], body["radius"], body["mass"], image_path=body["sprite"])
        newBody.isStatic = body["static"]
        celestial_bodies.add(newBody)

    #load in moons and assign them to the appropriate planet
    moons.empty()
    for moon in level_data["moons"]:
        newMoon = CelestialBody(moon["x"], moon["y"], moon["radius"], moon["mass"], image_path=moon["sprite"])
        newMoon.velocity = Helpers.calculate_orbital_velocity(newMoon, celestial_bodies.sprites()[moon["parent"]])
        newMoon.isStatic = moon["static"]
        celestial_bodies.sprites()[moon["parent"]].moons.add(newMoon)
        moons.add(newMoon)

    #load in targets
    targets.empty()
    for target in level_data["targets"]:
        newTarget = Target.Target(target["x"], target["y"], target["radius"])
        targets.add(newTarget)

    #add moons and planets into one group for calculation purposes
    all_bodies.empty()
    all_bodies.add(celestial_bodies, moons)

initialize()
clock = pygame.time.Clock()
player1 = player.Player((0, 255, 0), celestial_bodies.sprites()[0], celestial_bodies.sprites()[0].radius, playernum="1")
player1.id = 1
player2 = player.Player((0, 255, 0), celestial_bodies.sprites()[1], celestial_bodies.sprites()[1].radius, playernum="2")
player2.id = 2

#Time spent in menu
startMenuTime = pygame.time.get_ticks()//1000
prev_game = 0


players = [player1, player2]

while running:
    # delta time variable to keep track of time between frames
    dt = clock.tick(120) / 1000.0
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_h:
                controlsOpen = not controlsOpen
            if event.key == pygame.K_ESCAPE:
                initialize()
                reinitialize_player(player1)
                reinitialize_player(player2)
                playerTurn = 1
                prev_game = pygame.time.get_ticks() // 1000 - startMenuTime

        if event.type == pygame.QUIT:
            running = False

        else:
            for player in players:
                if playerTurn == player.id and player.health > 0:
                    player.handle_event(event)
                    if player.shot:
                        player.shot = False
                        playerTurn -= 1

    screen.blit(bg, bg_rect)
    projectiles = pygame.sprite.Group(player1.projectiles, player2.projectiles)
    celestial_bodies.update(dt, projectiles, all_bodies)
    targets.update(dt, projectiles)
    for player in players:
        #if player health if greater then 0
        if player.health > 0:
            player.draw(screen, all_bodies)
        else:
            mainmenu.end(screen, player.playernum, pygame.time.get_ticks()//1000 - prev_game - startMenuTime)
            initialize()
            reinitialize_player(player1)
            reinitialize_player(player2)
            playerTurn = 1
            prev_game = pygame.time.get_ticks() // 1000 - startMenuTime


        if player.id == playerTurn:
            player.update(dt, all_bodies)
            targets.update(dt, player.projectiles)
        for other_player in players:
            if other_player.id != player.id:
                other_player.projectiles.update(dt, all_bodies)
                targets.update(dt, other_player.projectiles)
                other_player.update_position()
                player.hit(other_player)

    all_bodies.draw(screen)
    targets.draw(screen)

    #Draw gui on top of everything
    for player in players:
        if player.id == playerTurn and player.health > 0:
            player.draw_gui(screen)
        #if player.health == 0:
            #running = False

    #Draw controls on screen and timer on screen
    gui.draw_controls(screen, constants.WHITE, controlsOpen)
    gui.draw_timer(screen, constants.WHITE, pygame.time.get_ticks()//1000 - prev_game - startMenuTime)


    if playerTurn <= 0:
        playerTurn = playerCount
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()