import pygame
import constants
import gui

title = pygame.image.load("Sprites/titlescreen.png")
title = pygame.transform.scale(title, (constants.Width, constants.Height))
t_rect = title.get_rect()

loadscreen = pygame.image.load("Sprites/selectscreen.png")
loadscreen = pygame.transform.scale(loadscreen, (constants.Width, constants.Height))
ls_rect = loadscreen.get_rect()

endscreen = pygame.image.load("Sprites/endscreen.png")
endscreen = pygame.transform.scale(endscreen, (constants.Width, constants.Height))
end_rect = loadscreen.get_rect()

quitbuttonImg = pygame.image.load("Sprites/quitbutton.png")
levelbuttonImg = pygame.image.load("Sprites/levelbutton.png")
quitbuttondownImg = pygame.image.load("Sprites/quitbuttondown.png")
levelbuttondownImg = pygame.image.load("Sprites/levelbuttondown.png")

l1upImg = pygame.image.load("Sprites/l1up.png")
l1downImg = pygame.image.load("Sprites/l1down.png")
l2upImg = pygame.image.load("Sprites/l2up.png")
l2downImg = pygame.image.load("Sprites/l2down.png")
l3upImg = pygame.image.load("Sprites/l3up.png")
l3downImg = pygame.image.load("Sprites/l3down.png")

backupImg = pygame.image.load("Sprites/backbuttonup.png")
backdownImg = pygame.image.load("Sprites/backbuttondown.png")

restart_buttonImg = pygame.image.load("Sprites/backbuttonup.png")
restart_buttonImgDown = pygame.image.load("Sprites/backbuttondown.png")




# Button class for ease of making buttons
class Button:
    def __init__(self, width, height, x, y, color, text, screen, fontsize, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.color = color
        if image != "":
            self.image = pygame.transform.scale(image, (width, height))
        self.enabled = True
        self.fontsize = fontsize
        self.font = pygame.font.SysFont('Corbel', fontsize)
        self.contents = text
        self.text = self.font.render(text, True, 'white')
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.text, (self.rect.x + (self.rect.width / 2) - (self.font.size(self.contents)[0] / 2)
                                    ,self.rect.y + (self.rect.height / 2) - (self.font.size(self.contents)[1] / 2) ) )

    def changeImage(self, img):
        self.image = pygame.transform.scale(img, (self.width,self.height))

    def clicked(self):
        mouse = pygame.mouse.get_pos()
        if (self.enabled and
            self.rect.x < mouse[0] < (self.rect.x + self.rect.width) and
            self.rect.y < mouse[1] < (self.rect.y + self.rect.height)):
            return True
        else:
            return False

def menu(screen):
    # Initialize buttons
    startbutton = Button(200, 100, screen.get_width()/2 - 100, screen.get_height()/2 - 50, 'black', "level select", screen, 40, levelbuttonImg)
    quitbutton = Button(200, 100, screen.get_width() / 2 - 100, screen.get_height() / 2 + 150, 'black', "quit", screen, 40, quitbuttonImg)

    startbuttonDown = False
    quitbuttonDown = False
    while True:
        screen.blit(title, t_rect)
        for event in pygame.event.get():

            #If button is pressed, change image to show that
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Put possible button click events here
                if startbutton.clicked():
                    startbuttonDown = True
                    startbutton.changeImage(levelbuttondownImg)
                if quitbutton.clicked():
                    quitbuttonDown = True
                    quitbutton.changeImage(quitbuttondownImg)

            #If button is let go of while being pressed do said buttons action
            if event.type == pygame.MOUSEBUTTONUP:
                if startbutton.clicked() and startbuttonDown == True:
                    level = level_select(screen)
                    startbutton.changeImage(levelbuttonImg)
                    quitbutton.enabled = False
                    if level != "":
                        return level
                elif quitbutton.clicked() and quitbuttonDown == True:
                    pygame.quit()
                else:
                    startbuttonDown = False
                    quitbuttonDown = False
                    startbutton.changeImage(levelbuttonImg)
                    quitbutton.changeImage(quitbuttonImg)


            if event.type == pygame.QUIT:
                pygame.quit()

        # Draw everything on the main menu
        screen.blit(startbutton.image, startbutton.rect)
        screen.blit(quitbutton.image, quitbutton.rect)
        quitbutton.enabled = True
        pygame.display.flip()

def level_select(screen):
    # Initialize buttons
    levelI = Button(200, 100, screen.get_width() / 2 - 350, screen.get_height() / 2 - 150, 'black', "Level I",
                         screen, 40,l1upImg)
    levelY = Button(200, 100, screen.get_width() / 2 - 100, screen.get_height() / 2 - 150, 'black', "Level Y",
                          screen, 40,l2upImg)
    levelD = Button(200, 100, screen.get_width() / 2 + 150, screen.get_height() / 2 - 150, 'black', "Level D",
                    screen, 40,l3upImg)
    quitbutton2 = Button(200, 100, screen.get_width() / 2 - 100, screen.get_height() / 2 + 50, 'black', "Back", screen,
                        40,backupImg)

    l1down = False
    l2down = False
    l3down = False
    backdown = False
    while True:
        screen.blit(loadscreen, ls_rect)
        for event in pygame.event.get():
            # If button is pressed, change image to show that
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Put possible button click events here
                if levelI.clicked():
                    l1down = True
                    levelI.changeImage(l1downImg)
                if levelY.clicked():
                    l2down = True
                    levelY.changeImage(l2downImg)
                if levelD.clicked():
                    l3down = True
                    levelD.changeImage(l3downImg)
                if quitbutton2.clicked():
                    backdown = True
                    quitbutton2.changeImage(backdownImg)

            # If button is let go of while being pressed do said buttons action
            if event.type == pygame.MOUSEBUTTONUP:
                if levelI.clicked() and l1down == True:
                    levelI.changeImage(l1upImg)
                    return "Levels/IanLevel.json"
                elif levelY.clicked() and l2down == True:
                    levelY.changeImage(l2upImg)
                    return "Levels/Level_Yurii.json"
                elif levelD.clicked() and l3down == True:
                    levelD.changeImage(l3upImg)
                    return "Levels/DomLevel.json"
                elif quitbutton2.clicked() and backdown == True:
                    quitbutton2.changeImage(backupImg)
                    return ""

                else:
                    l1down = False
                    l2down = False
                    l3down = False
                    backdown = False

                    levelI.changeImage(l1upImg)
                    levelY.changeImage(l2upImg)
                    levelD.changeImage(l3upImg)
                    quitbutton2.changeImage(backupImg)

            if event.type == pygame.QUIT:
                pygame.quit()




        # Draw everything on the main menu
        screen.blit(levelI.image, levelI.rect)
        screen.blit(levelY.image, levelY.rect)
        screen.blit(levelD.image, levelD.rect)
        screen.blit(quitbutton2.image, quitbutton2.rect)
        pygame.display.flip()

def end(screen, playernum, time):
    restart_button = Button(200, 100, screen.get_width() / 2 - 100, screen.get_height() / 2 + 150, 'black', "quit", screen,
                        40, restart_buttonImg)


    restart_button_down = False
    while True:
        screen.blit(endscreen, t_rect)
        gui.playerwin(screen, playernum, time)
        for event in pygame.event.get():

            # If button is pressed, change image to show that
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Put possible button click events here
                if restart_button.clicked():
                    restart_button_down = True
                    restart_button.changeImage(restart_buttonImgDown)

            # If button is let go of while being pressed do said buttons action
            if event.type == pygame.MOUSEBUTTONUP:
                if restart_button.clicked() and restart_button_down == True:
                    return
                else:
                    restart_button_down = False
                    restart_button.changeImage(restart_buttonImg)

            if event.type == pygame.QUIT:
                pygame.quit()

        # Draw everything on the main menu
        screen.blit(restart_button.image, restart_button.rect)
        pygame.display.flip()