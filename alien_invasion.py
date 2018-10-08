import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from scoreboard import Scoreboard
from game_stats import GameStats
from button import Button
from MainMenu import MainMenu
from bunker import Bunker
import game_functions as gf

def run_game():
    # initialize pygame, settings, and screen object
    pygame.mixer.pre_init(22050, -16, 2, 512)
    pygame.mixer.init()
    pygame.init()
    laser = pygame.mixer.music
    crash = pygame.mixer.music

    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    #make the play button
    play_button = Button(ai_settings, screen, "Play")

    #create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    #Make a ship, a group of bullets and a group of aliens
    ship = Ship(ai_settings,screen)

    #Make a group to store bullets in
    bullets = Group()
    alienBullets = Group()
    aliens = Group()
    motherships = Group()
    bunkers = Group()

    #create the fleet of aliens.
    gf.create_fleet(ai_settings,screen,ship,aliens)
    gf.create_bunkers(ai_settings,screen,ship,aliens,bunkers)
    
    bg_color = (230,230,230)

    mainMenu = MainMenu(screen)
    mainMenu.wait()

    #start the main loop for the game.
    while True:
        gf.check_events(ai_settings,screen,stats,sb, play_button,ship,aliens, bullets,alienBullets,bunkers,motherships,laser,crash)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen,stats, sb, ship, aliens, bullets,alienBullets,bunkers,motherships,crash)
            gf.update_aliens(ai_settings,screen, stats, sb, ship, aliens, bullets,motherships)
            gf.update_bunkers(ai_settings,screen,sb,ship,aliens,bullets,bunkers)
        
        gf.update_screen(ai_settings,screen,stats,sb, ship,aliens,bullets,play_button,alienBullets,bunkers,motherships)

run_game()