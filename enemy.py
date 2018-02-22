import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/smallPlane.png").convert_alpha()
        self.destroy_image = pygame.image.load("image/smallPlaneDestroy.png").convert_alpha()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect = self.image.get_rect()
        self.rect.left ,self.rect.top = randint(0,self.width - self.rect.width),\
                                        randint((-5) * self.height,0)
        self.speed = 2
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)


    def move(self):
        if self.rect.top <= self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left ,self.rect.top = randint(0,self.width - self.rect.width),\
                                        randint((-5)* self.height,0)
        self.active = True


class MidEnemy(pygame.sprite.Sprite):
    energy = 6
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/middlePlane.png").convert_alpha()
        self.destroy_image = pygame.image.load("image/middlePlaneDestroy.png").convert_alpha()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect = self.image.get_rect()
        self.rect.left ,self.rect.top = randint(0,self.width - self.rect.width),\
                                        randint((-10) * self.height,-self.height)
        self.speed = 2
        self.active = True
        self.energy = MidEnemy.energy
        self.mask = pygame.mask.from_surface(self.image)


    def move(self):
        if self.rect.top <= self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left ,self.rect.top = randint(0,self.width - self.rect.width),\
                                        randint((-10) * self.height,-self.height)
        self.active = True
        self.energy = MidEnemy.energy
        

class BigEnemy(pygame.sprite.Sprite):
    energy = 15
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("image/bigPlane1.png").convert_alpha()
        self.image2 = pygame.image.load("image/bigPlane2.png").convert_alpha()
        self.destroy_image = pygame.image.load("image/bigPlaneDestroy.png").convert_alpha()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect = self.image1.get_rect()
        self.rect.left ,self.rect.top = randint(0,self.width - self.rect.width),\
                                        randint((-15) * self.height,(-5) * self.height)
        self.speed = 2
        self.active = True
        self.energy = BigEnemy.energy
        self.mask = pygame.mask.from_surface(self.image1)
        self.mask = pygame.mask.from_surface(self.image2)


    def move(self):
        if self.rect.top <= self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left ,self.rect.top = randint(0,self.width - self.rect.width),\
                                        randint((-15) * self.height,(-5) * self.height)
        self.active = True
        self.energy = BigEnemy.energy


class Boss(pygame.sprite.Sprite):
    energy = 200

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("boss\lv1.png").convert_alpha()
        self.image_hit = pygame.image.load("boss\lv1_hit.png").convert_alpha()

        self.size = bg_size
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = (-1 * self.rect.height), (self.size[0] - self.rect.width) // 2
        self.active = False
        self.hit = False
        self.speed = 1
        self.speed_level = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = Boss.energy
        self.game_lv = 1

    def move(self):
        # 由上方生成 移动到屏幕正上
        if self.rect.top < 0:
            self.rect.top += self.speed
        else:
            self.speed = 0
            self.rect.left += self.speed_level

            if self.rect.right >= self.size[0]:
                self.rect.right = self.size[0]
                self.speed_level = -self.speed_level

            if self.rect.left <= 0:
                self.rect.left = 0
                self.speed_level = -self.speed_level

    def reset(self):
        self.rect.top, self.rect.left = (-1 * self.rect.height), (self.size[0] - self.rect.width) // 2
        self.speed = 1

        self.speed_level += 0
        Boss.energy = 2.5 * Boss.energy
        self.energy = Boss.energy
        self.active = True

        self.image = pygame.image.load("boss\lv%d.png" % (self.game_lv)).convert_alpha()
        self.image_hit = pygame.image.load("boss\lv%s_hit.png" % (self.game_lv)).convert_alpha()
        self.game_lv += 1

    def _return(self):
        self.active = False
        self.rect.top, self.rect.left = (-1 * self.rect.height), (self.size[0] - self.rect.width) // 2







        
        


            
        
            
    
            
        
            
           
            
        
        
    
