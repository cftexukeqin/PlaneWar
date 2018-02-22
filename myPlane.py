import pygame

class Myplane(pygame.sprite.Sprite):
    
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.myplane_image1 = pygame.image.load("image/myplane1.png").convert_alpha()
        self.myplane_image2 = pygame.image.load("image/myplane2.png").convert_alpha()
        self.destroy_image = pygame.image.load("image/myPlaneDestroy.png").convert_alpha()
        self.rect = self.myplane_image1.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left ,self.rect.top = (bg_size[0] - self.rect.width) // 2,\
                                        bg_size[1] - self.rect.height - 50    
        self.speed = 10
        self.active = True
        self.invicible = False
        self.mask = pygame.mask.from_surface(self.myplane_image1)
        self.mask = pygame.mask.from_surface(self.myplane_image2)

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = -30

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width + 30
            
    def reset(self):
        self.rect.left ,self.rect.top = (self.width - self.rect.width) // 2,\
                                        self.height - self.rect.height - 50
        self.active = True
        self.invicible = True

class Protection_cover(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.bg_size = bg_size
        self.image = pygame.image.load("image/Pi1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, centerx, centery):
        self.rect.centerx, self.rect.centery = centerx,centery
        
