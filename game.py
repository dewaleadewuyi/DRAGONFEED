import pygame,random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

# display surface
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# caption
pygame.display.set_caption("feed the Dragon game")

# COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARKGREEN = (10,50,10)

# set fps and clock
fps = 60
clock = pygame.time.Clock()

# set game values (constant)
PLAYER_STARTING_LIVE = 1
PLAYER_VELOCITY = 5
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = -100

score = 0
player_lives = PLAYER_STARTING_LIVE
coin_velocity = COIN_STARTING_VELOCITY

# set fonts 
font = pygame.font.Font("./feed_the_dragon_assets/feed_the_dragon_assets/AttackGraffiti.ttf",32)

# set text
score_text = font.render("Score : "+ str(score),True,GREEN,DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

title_text = font.render("Feed The Dragon", True, GREEN, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

live_text = font.render("Lives : "+str(player_lives), True, GREEN, DARKGREEN)
live_rect = live_text.get_rect()
live_rect.topright = (WINDOW_WIDTH-10,10)

game_over_text = font.render("GAME OVER", True, GREEN,DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)


continue_text = font.render("press any key to continue", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2 +32)

# set sound
coin_sound = pygame.mixer.Sound("./feed_the_dragon_assets/feed_the_dragon_assets/coin_sound.wav")
miss_sound = pygame.mixer.Sound("./feed_the_dragon_assets/feed_the_dragon_assets/miss_sound.wav")
miss_sound.set_volume(.1)
pygame.mixer.music.load("./feed_the_dragon_assets/feed_the_dragon_assets/ftd_background_music.wav")

# set images
player_image = pygame.image.load("./feed_the_dragon_assets/feed_the_dragon_assets/dragon_right.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT//2

coin_image = pygame.image.load("./feed_the_dragon_assets/feed_the_dragon_assets/coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64,WINDOW_HEIGHT - 32)


pygame.mixer.music.play(-1,0.0)
running = True
while running:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
            
    # check to see if the player want to move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY
        
    # Move the coin
    if coin_rect.x< 0:
        # missed coin
        player_lives -=1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64,WINDOW_HEIGHT - 32)
        
    else:
        coin_rect.x -= coin_velocity
        
    if player_rect.colliderect(coin_rect):
        score +=1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64,WINDOW_HEIGHT - 32)
        
    # update the score and live by re-rendering
    score_text = font.render("Score : "+ str(score),True,GREEN,DARKGREEN)
    live_text = font.render("Lives : "+str(player_lives), True, GREEN, DARKGREEN)
    
    # check for game over
    if player_lives == 0:
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pygame.display.update()
        
        # pause the game until the player presses any key to reset
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # the player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVE
                    coin_velocity = COIN_STARTING_VELOCITY
                    player_rect.y = WINDOW_HEIGHT//2 
                    pygame.mixer.music.play(-1,0.0)
                    is_paused = False
                # the player wants to stop the game
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    
                
         
    
    # fill the display
    display_surface.fill(BLACK)
    
    # Blit Text to the surface
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(live_text,live_rect)
    
    pygame.draw.line(display_surface,WHITE,(0,64),(WINDOW_WIDTH,64),2)
    
    # blit the images
    display_surface.blit(player_image,player_rect)
    display_surface.blit(coin_image,coin_rect)
            

# update display and tick the clock
    pygame.display.update()
    clock.tick(fps)

# pygame quit
pygame.quit()
