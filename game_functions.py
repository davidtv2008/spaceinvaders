import sys
import pygame
from bullet import Bullet
from alienBullet import AlienBullet
from alien import Alien
from time import sleep
from bunker import Bunker
import random

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    #create an alien and find the numbers of aliens in a row
    #spacing between each alien is equal to one alien width
    alienName = 'alien3_0.gif'
    img = pygame.image.load("resources/images/alien3_0.gif")
    alien = Alien(ai_settings,screen,img,alienName)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    #create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number,alienName)

def create_bunkers(ai_settings,screen,ship,aliens,bunkers):
    '''create the 3 bunkers'''
    bunkerName = 'bunker1.gif'
    img = pygame.image.load('resources/images/bunker1.gif')

    #create 3 bunker group
    i = 0
    while i < 3:
        create_bunker(ai_settings,screen,bunkers,bunkerName,i)
        i += 1

def create_bunker(ai_settings,screen,bunkers,bunkerName,i):
    """Create a bunker and place it in the row"""
    img = pygame.image.load("resources/images/bunker"+str(i)+".gif")
    bunkerName = 'bunker'+str(i)+'.gif'

    bunker = Bunker(ai_settings,screen,img,bunkerName)
    if i == 0:
        bunker_width = bunker.rect.width
        bunker_height = bunker.rect.height
        bunker.rect.x = 250
        bunker.rect.y = 600
    elif i == 1:
        bunker_width = bunker.rect.width
        bunker_height = bunker.rect.height
        bunker.rect.x = 550
        bunker.rect.y = 600
    elif i ==2:
        bunker_width = bunker.rect.width
        bunker_height = bunker.rect.height
        bunker.rect.x = 850
        bunker.rect.y = 600

    bunkers.add(bunker)


def create_alien(ai_settings,screen,aliens,alien_number,row_number,alienName):
    """Create an alien and place it in the row"""
    img = pygame.image.load("resources/images/alien3_0.gif")
    alienName = 'alien3_0.gif'

    if row_number == 0:
        img = pygame.image.load("resources/images/alien3_0.gif")
        alienName = 'alien3_0.gif'
    elif row_number == 1 or row_number == 2:
        img = pygame.image.load("resources/images/alien1_0.gif")
        alienName = 'alien1_0.gif'
    elif row_number == 3:
        img = pygame.image.load("resources/images/alien2_0.gif")
        alienName = 'alien2_0.gif'

    alien = Alien(ai_settings, screen,img,alienName)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_mothership(ai_settings,screen,aliens,motherships):
    '''create mothership and have it spawn randomly'''
    img = pygame.image.load("resources/images/alien4_0.gif")
    alienName = 'alien4_0.gif'

    alien = Alien(ai_settings,screen,img,alienName)
    alien.x = 0
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 20
    motherships.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_aliens_x(ai_settings,alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def check_keydown_events(event,ai_settings,screen,ship,bullets,laser):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets,laser)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets,laser):
    """Fire a bullet if limit not reached yet"""
    # craete a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        #pygame.mixer.music.load('resources/sounds/laser.mp3')
        laser.load('resources/sounds/laser.mp3')
        laser.play()
        

def fireAlienBullet(ai_settings,screen,alien,bullets,laser):
    """Fire a bullet if limit not reached yet"""
    # craete a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        newAlienBullet = AlienBullet(ai_settings, screen, alien)
        bullets.add(newAlienBullet)
        laser.load('resources/sounds/laser.mp3')
        laser.play()
            

def check_events(ai_settings,screen, stats,sb, play_button,ship,aliens, bullets,alienBullets,bunkers,motherships,laser,crash):
    """Respond to keypresses and mouse events"""
    # watch for keyboard and mouse events.
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            if stats.high_score > 0:
                file = open('resources/highScore.txt', 'a+')
                file.write(str(stats.high_score)+'\r\n')
                file.close()

            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,laser)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type ==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats,sb, play_button,ship, aliens,bullets, mouse_x,mouse_y)
    
    for x in range(10):
        num = random.randint(1,2000)
        if num == 1000:
            fireFromSprite = random.randint(1,34)
            i = 0
            for y in aliens:
                if i == fireFromSprite:
                    fireAlienBullet(ai_settings,screen,y,alienBullets,laser)                    
                i += 1
    
    for x in range(10):
        num = random.randint(1,50000)
        if num == 10000:    
            create_mothership(ai_settings,screen,aliens,motherships)

        
def check_play_button(ai_settings, screen, stats,sb, play_button,ship, aliens, bullets, mouse_x,mouse_y):
    """Start a new game when the player click Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)

    if button_clicked and not stats.game_active:
        #Reset the game settings
        ai_settings.initialize_dynamic_settings()

        #Hide the mouse cursor
        pygame.mouse.set_visible(False)
        #reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        #reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_keyup_events(event,ship):
    """respond to key release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(ai_settings, screen, stats,sb, ship,aliens,bullets, play_button,alienBullets,bunkers,motherships):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    for alienBullet in alienBullets.sprites():
        alienBullet.draw_bullet()
    
    for bunker in bunkers.sprites():
        bunker.draw_bunker()
    

    ship.blitme()
    aliens.draw(screen)
    bunkers.draw(screen)
    motherships.draw(screen)

    #draw the score information
    sb.show_score()

    #Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen,stats,sb, ship, aliens, bullets,alienBullets,bunkers,motherships,crash):
    """update position of bullets and get rid of old bullets"""
    #Update bullet position.
    bullets.update()
    alienBullets.update()

    # get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    # get rid of bullets that have disappeared
    for alienBullet in alienBullets.copy():
        if alienBullet.rect.top >= 900:
            alienBullets.remove(alienBullet)
        
    check_bullet_bunker_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets,alienBullets,bunkers,crash)
    check_bullet_aliens_collisions(ai_settings,screen,stats, sb,ship,aliens,bullets,bunkers,motherships,crash)
    check_bullet_ship_collisions(ai_settings,screen,stats, sb,ship,aliens,alienBullets,crash)

def check_bullet_bunker_collisions(ai_settings, screen,stats, sb, ship, aliens, bullets,alienBullets,bunkers,crash):
    """Respond to bullet-bunker collision"""
    
    collisions1 = pygame.sprite.groupcollide(bullets, bunkers, True,True)
    collisions2 = pygame.sprite.groupcollide(alienBullets,bunkers,True,True)

    
    if collisions1:
        for bunkers in collisions1.values():
            bunker_hit(ai_settings,screen,sb,ship,aliens,bullets,bunkers)
            crash.load('resources/sounds/crash.mp3')
            crash.play()
    
    if collisions2:
        for bunkers in collisions2.values():
            bunker_hit(ai_settings,screen,sb,ship,aliens,bullets,bunkers)
            crash.load('resources/sounds/crash.mp3')
            crash.play()
    

def bunker_hit(ai_settings, screen, sb, ship, aliens,bullets,bunkers):
    """Respond to bunker being hit by bullet"""
    
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        #Decrement ship left
        stats.ships_left -= 1

        #update scoreboard
        sb.prep_ships()

        #empty the list of aliens and bullets
        #aliens.empty()
        bullets.empty()


        #create a new fleet and center the ship
        #create_fleet(ai_settings,screen, ship, aliens)
        ship.center_ship()

        #pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_bullet_ship_collisions(ai_settings, screen,stats, sb, ship, aliens, bullets,crash):
    """Respond to bullet-ship collision"""
    #remove any bullets and aliens that have collided
    #collisions = pygame.sprite.groupcollide(bullets, ship, True, True)
    collisions = pygame.sprite.spritecollide(ship, bullets, True)
    
    if collisions:
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
        crash.load('resources/sounds/crash.mp3')
        crash.play()

def check_bullet_aliens_collisions(ai_settings, screen,stats, sb, ship, aliens, bullets,bunkers,motherships,crash):
    """Respond to bullet-alien collision"""
    #remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    collisions2 = pygame.sprite.groupcollide(bullets,motherships,True,True)
    
    if collisions:
        for aliens in collisions.values():
            for a in aliens:
                if a.name == 'alien3_0.gif' or a.name == 'alien3_1.gif':
                    stats.score += 10
                elif a.name == 'alien1_0.gif' or a.name == 'alien1_1.gif':
                    stats.score += 20
                elif a.name == 'alien2_0.gif' or a.name == 'alien2_1.gif':
                    stats.score += 40
                elif a.name == 'alien4_0.gif' or a.name == 'alien4_1.gif':
                    stats.score += 100
            sb.prep_score()
        check_high_score(stats,sb)
        crash.load('resources/sounds/crash.mp3')
        crash.play()
    
    if collisions2:
        for aliens in collisions2.values():
            for a in aliens:
                if a.name == 'alien4_0.gif' or a.name == 'alien4_1.gif':
                    stats.score += 100
            sb.prep_score()
        check_high_score(stats,sb)
        crash.load('resources/sounds/crash.mp3')
        crash.play()

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        motherships.empty()
        ai_settings.increase_speed()

        #Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)
        create_bunkers(ai_settings,screen,ship,aliens,bunkers)

def check_fleet_edges(ai_settings,aliens,motherships):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
    
    for alien in motherships.sprites():
        if alien.check_edges():
            change_mothership_direction(ai_settings,motherships)
            break

def change_mothership_direction(ai_settings, aliens):
    """change the mothership direction."""
    ai_settings.mothership_direction *= -1


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def update_bunkers(ai_settings,screen, sb, ship, aliens, bullets,bunkers):
    """Check if the fleet is at an edge, and then update the postions of all aliens in the fleet."""
    #check_fleet_edges(ai_settings, aliens)
    bunkers.update()

    if pygame.sprite.groupcollide(bullets, bunkers, True, True):
        bunker_hit(ai_settings,screen,sb, ship, aliens, bullets,bunkers)

def update_aliens(ai_settings,screen, stats, sb, ship, aliens, bullets,motherships):
    """Check if the fleet is at an edge, and then update the postions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens,motherships)
    aliens.update()
    motherships.update()

    # look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb, ship, aliens, bullets)
    
    #look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #treat this the same as if the ship got hit.
            ship_hit(ai_settings,screen, stats, sb, ship, aliens, bullets)
            break
    
def check_high_score(stats,sb):
    """Check to see if theres a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()