import pygame
import sys
from pygame.sprite import Sprite

class MainMenu(Sprite):
    
    def __init__(self,screen):

        super(MainMenu,self).__init__()

        #create some attributes and setup text for main menu
        #"SPACE" text
        self.textColor1 = (255,255,255)
        self.font1 = pygame.font.SysFont(None, 100)

        self.screen = screen

        #"INVADERS" text
        self.textColor2 = (100,183,30)
        self.font2 = pygame.font.SysFont(None,80)

        #create my actual text for the title and set its color and background color
        self.title1 = self.font1.render("SPACE", True, self.textColor1, (0,0,0))
        self.title1Rect = self.title1.get_rect()
        self.title1Rect.center = (screen.get_rect().centerx,screen.get_rect().top + 100)
        
        self.title2 = self.font2.render("INVADERS",True,self.textColor2,(0,0,0))
        self.title2Rect = self.title2.get_rect()
        self.title2Rect.center = (self.title1Rect.centerx,self.title1Rect.bottom + (self.title1Rect.bottom - self.title1Rect.centery))
        


        #load the sprites and get their sizes
        numberAliens = 4
        self.image = [None] * numberAliens
        self.imgRect = [None] * numberAliens
        self.point = [None] * numberAliens
        self.pointRect = [None] * numberAliens
        self.font3 = pygame.font.SysFont(None,40)
        
        for x in range(numberAliens):
            self.image[x] = pygame.image.load('resources/images/alien'+str(x)+'.gif')
            self.imgRect[x] = self.image[x].get_rect()

            if x == 0:
                self.point[x] = self.font3.render("= 10",True,self.textColor1,(0,0,0))
            elif x == 1:
                self.point[x] = self.font3.render("= 20",True,self.textColor1,(0,0,0))
            elif x == 2:
                self.point[x] = self.font3.render("= 40",True,self.textColor1,(0,0,0))
            elif x == 3:
                self.point[x] = self.font3.render("= ??",True,self.textColor1,(0,0,0))

            self.pointRect[x] = self.point[x].get_rect()
            if x == 0:
                self.imgRect[x].center = (self.title1Rect.centerx - 40,self.title2Rect.bottom + (self.title2Rect.bottom - self.title2Rect.centery))
                self.pointRect[x].center = (self.title1Rect.centerx + 40,self.title2Rect.bottom + (self.title2Rect.bottom - self.title2Rect.centery))
            else:
                self.imgRect[x].center = (self.title1Rect.centerx - 40,self.imgRect[x-1].bottom + (self.imgRect[x-1].bottom - self.imgRect[x-1].centery))
                self.pointRect[x].center = (self.title1Rect.centerx + 40,self.imgRect[x-1].bottom + (self.imgRect[x-1].bottom - self.imgRect[x-1].centery))
           
        #play button to start game
        self.start = self.font2.render("Play Game", True, self.textColor2, (0,0,0))
        self.startRect = self.start.get_rect()
        self.startRect.center = (screen.get_rect().centerx, self.imgRect[3].bottom + 40 + (self.imgRect[3].bottom - self.imgRect[3].centery))
        self.rect = pygame.Rect(self.startRect.left,self.startRect.top, self.startRect.width, self.startRect.height)
        self.play = False

        #highscores button to start game
        self.highScore = self.font2.render("Highest Score", True, self.textColor2, (0,0,0))
        self.highRect = self.highScore.get_rect()
        self.highRect.center = (screen.get_rect().centerx, self.imgRect[3].bottom + 130)
        self.highrect = pygame.Rect(self.highRect.left,self.highRect.top, self.highRect.width, self.highRect.height)
        self.score = False
        self.scores = []
        self.highestScore = 0

        self.addAll()
        

    def addAll(self):
        self.addGameObject(self.screen,self.title1,self.title1Rect)
        self.addGameObject(self.screen,self.title2,self.title2Rect)
        self.addGameObject(self.screen,self.image[0],self.imgRect[0])
        self.addGameObject(self.screen,self.image[1],self.imgRect[1])
        self.addGameObject(self.screen,self.image[2],self.imgRect[2])
        self.addGameObject(self.screen,self.image[3],self.imgRect[3])
        self.addGameObject(self.screen,self.point[0],self.pointRect[0])
        self.addGameObject(self.screen,self.point[1],self.pointRect[1])
        self.addGameObject(self.screen,self.point[2],self.pointRect[2])
        self.addGameObject(self.screen,self.point[3],self.pointRect[3])
        self.addGameObject(self.screen,self.start,self.startRect)
        self.addGameObject(self.screen,self.highScore,self.highRect)
        


    def wait(self):
        while self.play == False:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type ==pygame.MOUSEBUTTONDOWN:
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    self.check_play_button(mouse_x,mouse_y)
                    self.check_score_button(mouse_x,mouse_y)
                        
            pygame.display.flip()    

    def displayHighScore(self):
        file = open('resources/highScore.txt', 'r')
        f1 = file.readlines()
        for x in f1:
            self.scores.append(int(x))
        file.close()

        if len(self.scores) == 0:
            print("no scores to show")
        elif len(self.scores) == 1:
            self.highestScore = self.scores[0]
        elif len(self.scores) > 1:
            i = 0
            self.highestScore = self.scores[0]
            while i < len(self.scores):
                if self.highestScore < self.scores[i+1]:
                    self.highestScore = self.scores[i+1]
                i += 1
                if i == len(self.scores)-1:
                    break
        open('resources/highScore.txt', 'w').close()
        file = open('resources/highScore.txt','w')
        file.write(str(self.highestScore)+'\r\n')

        self.hs = self.font2.render(str(self.highestScore),True,self.textColor2,(0,0,0))
        self.hsRect = self.hs.get_rect()
        self.hsRect.center = (self.screen.get_rect().centerx, self.imgRect[3].bottom + 290)
        self.addGameObject(self.screen,self.hs,self.hsRect)
               

    def check_play_button(self,mouse_x,mouse_y):
        """Start a new game when the player click Play."""
        button_clicked = self.rect.collidepoint(mouse_x,mouse_y)

        if button_clicked:
            self.play = True
        
    def check_score_button(self,mouse_x,mouse_y):
        """Start a new game when the player click Play."""
        button_clicked = self.highrect.collidepoint(mouse_x,mouse_y)

        if button_clicked:
            self.displayHighScore()


    def addGameObject(self,screen,object,xy):
        #print(len(object))
        screen.blit(object,xy)  