try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
except ImportError as err:
    import sys, os, pygame
    print(f"couldn't load module. {err}")
    sys.exit(2)

def load_png(name):
    fullname = os.path.join('Sprites', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print(f"Cannot load image: {name}")
        raise SystemExit(message)
    return image, image.get_rect()
