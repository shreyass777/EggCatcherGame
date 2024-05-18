import pygame as pg
import random

# Initialise Pygame
pg.init()
state = "Start"

# Crreate screen
screen_width = 800
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))

# Title and Icon
pg.display.set_caption("Egg Catcher")
icon = pg.image.load("EggIcon.png")
pg.display.set_icon(icon)

# Background Image
bg_day = pg.image.load("Day.jpg").convert()
bg_day = pg.transform.scale(bg_day, (screen_width, screen_height))
bg_night = pg.image.load("Night.jpg").convert()
bg_night = pg.transform.scale(bg_night, (screen_width, screen_height))

# Basket
basket_width = 64
basket_height = 36
basketImgs = [pg.image.load("basket3.png"),pg.image.load("basket2.png"),pg.image.load("basket1.png")]
basketImg = basketImgs[0]
basketX = screen_width // 2 - basket_width // 2
basketY = 480

# Egg
eggs = []
egg_width = 24
egg_height = 32
eggImg = pg.image.load("Egg.png")
egg_speed = 1
egg_spawn_interval = 100
spawn_timer = egg_spawn_interval

score = 0
lives_remaining = 3
quit_timer = 1
font = pg.font.SysFont(None, 30)

def create_eggs():
    eggX = random.randint(10,screen_width-egg_width)
    eggY = random.randint(10,30)
    eggs.append([eggX,eggY])

clock = pg.time.Clock()

def switch_background(score):
    if score < 10:
        screen.blit(bg_day, (0, 0))
    else:
        screen.blit(bg_night, (0, 0))
        
def switch_basket(score):
    global basketImg
    if score < 15:
        basketImg = basketImgs[0]
    elif score < 30:
        basketImg = basketImgs[1]
    else:
        basketImg = basketImgs[2]

# Game Loop
while state != "Close":
    
    if quit_timer == 0:
        break
    
    # Background Image
    switch_background(score)
    
    # Quit Game
    for event in pg.event.get():
        if event.type == pg.QUIT:
            state = "Close"
    
    if state == "Start":
        intro_text = font.render(f"Welcome to Egg Catcher", True, (0, 0, 255))
        screen.blit(intro_text, (screen_width // 2 - 130, screen_height // 2 - 150))
        control_text = font.render(f"Press P to Pause", True, (0, 0, 255))
        screen.blit(control_text, (screen_width // 2 - 90, screen_height // 2 - 120))
        control_text = font.render(f"Press R to Resume", True, (0, 0, 255))
        screen.blit(control_text, (screen_width // 2 - 100, screen_height // 2 - 90))
        control_text = font.render(f"Press Enter to Continue", True, (0, 0, 255))
        screen.blit(control_text, (screen_width // 2 - 127, screen_height // 2 - 60))
    elif state == "Pause":
        pause_text = font.render("Press R to Resume", True, (0, 0, 255))
        screen.blit(pause_text, (screen_width // 2 - 100, screen_height // 2 - 90))
    elif state == "Quit":
        game_over_text = font.render("Game Over!", True, (0, 0, 255))
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 100))
        game_over_text = font.render(f"Your score is: {score}", True, (0, 0, 255))
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 80))
        quit_timer -= 1
    
    pg.display.flip()
    
    keys = pg.key.get_pressed()
    if keys[pg.K_q]:
        break
    elif (state == "Start" and keys[pg.K_RETURN]):
        state = "Play"
    elif (state == "Pause" and keys[pg.K_r]):
        state = "Play"
    elif (state == "Quit" and keys[pg.K_RETURN]):
        state = "Close"

    while state == "Play":
        
        # Background Image
        switch_background(score)
        
        # Basket Image
        switch_basket(score)
        
        # Quit Game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                state = "Close"
                break

        # Basket Movement
        keys = pg.key.get_pressed()
        if (keys[pg.K_q]):
            state = "Close"
        if (keys[pg.K_p]):
            state = "Pause"
            break
        if (keys[pg.K_RIGHT] and basketX < screen_width-basket_width):
            basketX += 8
        if (keys[pg.K_LEFT] and basketX > 0):
            basketX -= 8
        if (keys[pg.K_UP] and basketY > screen_height // 2):
            basketY -= 4
        if (keys[pg.K_DOWN] and basketY < screen_height-basket_height):
            basketY += 4
        
        #Spawn Eggs
        spawn_timer -= 1
        if spawn_timer == 0:
            create_eggs()
            spawn_timer = egg_spawn_interval
        
        # Move Eggs
        for egg in eggs:
            egg[1] += egg_speed
            screen.blit(eggImg, egg)
            
            # Collection detection
            if egg[1] > basketY - egg_height and egg[1] < basketY + basket_height:
                if basketX < egg[0] and egg[0] + egg_width < basketX + basket_width:
                    score += 1
                    eggs.remove(egg)
            if egg[1] == screen_height - egg_height:
                lives_remaining -= 1
                eggs.remove(egg)
        
        # Draw Basket
        screen.blit(basketImg, (basketX, basketY))
        
        # Display score and remaining lives
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives_remaining}", True, (255, 255, 255))
        screen.blit(lives_text, (screen_width - 120, 10))
        screen.blit(score_text, (10, 10))
        
        # Check for game over
        if lives_remaining == 0:
            game_over_text = font.render("Game Over!", True, (0, 0, 255))
            screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 100))
            game_over_text = font.render(f"Your score is: {score}", True, (0, 0, 255))
            screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 80))
            pg.display.flip()
            state = "Quit"
            quit_timer = 20000
            # pg.time.delay(30000)
        
        pg.display.flip()
        clock.tick(60)
        
pg.quit()