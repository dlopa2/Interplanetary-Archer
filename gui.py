import pygame
from sympy.printing.numpy import const

import constants

def draw_text(text, col, x, y, screen, img, amount, playernum, ratio):
    font = pygame.font.SysFont('Futura', 30)
    textImg = font.render(text, True, col)

    #Depending on player, display health and ammo on different sides of screen
    if playernum == "1":
        screen.blit(textImg, (x, y))
        for i in range(amount):
            screen.blit(pygame.transform.scale(img, (50 * ratio[0], 50 * ratio[1])), ((x + textImg.get_width()) + (i * (60 * ratio[0])), y-25))
    elif playernum == "2":
        screen.blit(textImg, (constants.Width - x - textImg.get_width(), constants.Height - y))
        for i in range(amount):
            screen.blit(pygame.transform.scale(img, (50 * ratio[0], 50 * ratio[1])), ((constants.Width - 50  * ratio[0] - (textImg.get_width())) + (i * (-60 * ratio[0])), constants.Height - y-25))

def draw_playernum(player, col, screen):
    font = pygame.font.SysFont('Futura', 30)
    textImg = font.render("Player " + player, True, col)
    screen.blit(textImg, (constants.Width/2 - 50, 25))

def draw_controls(screen, col, isOpen):
    count = 0
    font = pygame.font.SysFont('Futura', 30)

    #Display controls if player has pressed H
    if isOpen:
        text = ["Controls (Press H to close):", "--------------------", "1-5 to change arrow type (1:Arrow, 2:Rocket, 3:Scatter Arrow, 4:Spaceship, 5:Blackhole)", "A to move counter clockwise",
                "D to move clockwise", "Click and drag left mouse button to aim, release to fire", "ESC to return to main menu"]
    else:
        text = ["Press H to open controls"]

    #Blit from list onto screen
    for i in reversed(text):
        count += 1
        textImg = font.render(i, True, col)
        screen.blit(textImg, (10, constants.Height - 10 - (count * textImg.get_height())))


def draw_timer(screen, col, sec):
    font = pygame.font.SysFont('Futura', 30)
    text = "Time: " + str(sec) + " seconds"
    textImg = font.render(text, True, col)
    screen.blit(textImg, (constants.Width - textImg.get_width() - 10, 10))

def playerwin(screen, playernum, time):
    font = pygame.font.SysFont('Futura', 100)

    #Depending on which player has won, display number and different color
    if playernum == "1":
        text = "Player 2 Has Won!"
        textImg = font.render(text, True, constants.RED)
        screen.blit(textImg, (constants.Width / 2 - textImg.get_width() / 2, constants.Height / 2 - textImg.get_height() / 2))
        text = "Time: " + str(time)
        textImg = font.render(text, True, constants.RED)
        screen.blit(textImg,(constants.Width / 2 - textImg.get_width() / 2, constants.Height / 2 + (textImg.get_height()) / 2))
    else:
        text = "Player 1 Has Won!"
        textImg = font.render(text, True, constants.BLUE)
        screen.blit(textImg, (constants.Width / 2 - textImg.get_width() / 2, constants.Height / 2 - textImg.get_height() / 2))
        text = "Time: " + str(time)
        textImg = font.render(text, True, constants.BLUE)
        screen.blit(textImg, (constants.Width / 2 - textImg.get_width() / 2, constants.Height / 2 + (textImg.get_height()) / 2))





