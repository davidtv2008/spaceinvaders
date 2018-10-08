import pygame
from pygame.sprite import Sprite

class Bunker(Sprite):

    def __init__(self,ai_settings,screen,img,bunkerName):
        super(Bunker,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = img
        self.name = bunkerName

        self.maxHits = 6

        self.rect = self.image.get_rect()

        #start bunker below on top of ship
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image,self.rect)

    def check_edges(self):
        """Return True if alien is at the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        
    def draw_bunker(self):
        self.screen.blit(self.image,self.rect)