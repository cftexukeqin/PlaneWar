import pygame
from random import *

class BombSupply(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/bombSupply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left ,self.rect.top = randint(0,self.width - self.rect.width),-100
        self.active = False
        self.speed  = 3
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False
    def reset(self):
        self.active = True
        self.rect.left ,self.rect.top = randint(0,self.width - self.rect.width),-100

class SuperbulletSupply(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/bulletSupply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),-100
        self.active = False
        self.speed = 3
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False
    def reset(self):
        self.active = True
        self.rect.left ,self.rect.top = randint(0,self.width - self.rect.width),-100
        
