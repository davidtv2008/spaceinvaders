import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self,ai_settings,screen,img,alienName):
        """Initialize the alien and set its starting position"""
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load the alien image and set its rect attribute
        self.image = img
        self.name = alienName
        
        #self.image = pygame.image.load('resources/images/alien1_0.gif')
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image,self.rect)

    def check_edges(self):
        """Return True if alien is at the edge of screen"""
        if self.name == 'alien4_0.gif':
            return True
        else:
            screen_rect = self.screen.get_rect()
            if self.rect.right >= screen_rect.right:
                return True
            elif self.rect.left <= 0:
                return True



    def update(self):
        """Move the alien right or left."""

        if self.name =='alien4_0.gif':
            self.x += 1
            
        else:
            tempx = self.x
            self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        
            if tempx < self.x:
                if self.name == 'alien1_1.gif':
                    self.image = pygame.image.load("resources/images/alien1_0.gif")
                    self.name = 'alien1_0.gif'
                elif self.name == 'alien2_1.gif':
                    self.image = pygame.image.load("resources/images/alien2_0.gif")
                    self.name = 'alien2_0.gif'
                elif self.name == 'alien3_1.gif':
                    self.image = pygame.image.load("resources/images/alien3_0.gif")
                    self.name = 'alien3_0.gif'
            elif tempx > self.x:
                if self.name == 'alien1_0.gif':
                    self.image = pygame.image.load("resources/images/alien1_1.gif")
                    self.name = 'alien1_1.gif'
                elif self.name == 'alien2_0.gif':
                    self.image = pygame.image.load("resources/images/alien2_1.gif")
                    self.name = 'alien2_1.gif'
                elif self.name == 'alien3_0.gif':
                    self.image = pygame.image.load("resources/images/alien3_1.gif")
                    self.name = 'alien3_1.gif'
        self.rect.x = self.x
