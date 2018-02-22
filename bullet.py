import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__

        #普通子弹
        self.image = pygame.image.load("image/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()        
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.speed = 15
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self,position):
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.active = True
        

class SuperBullet(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__

        #厉害的子弹
        self.image = pygame.image.load("image/bullet2.png").convert_alpha()
        self.rect = self.image.get_rect()        
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.speed = 20
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)


    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self,position):
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.active = True
        
        
