# Randomly generating coins with different weights on the road
# Increase the speed of Enemy when the player earns N coins
# Comment code

import pygame
from pygame.locals import *
import random
import sys
import time

#initialize pygame
pygame.init()

#background vibe music
pygame.mixer.music.load('tokyo_drift.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


# FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# speed and points variables
SPEED = 5
SCORE = 0
POINTS = 0
CYCLE = 1
COIN_WEIGHTS = [1, 0.5, 2]  # Weights for different types coins
COIN_WEIGHT_TOTAL = sum(COIN_WEIGHTS)

# screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Load game background
bg = pygame.image.load("AnimatedStreet.png")

# display surface
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)

# fonts
font = pygame.font.Font("Lato-Black.ttf", 60)
font_small = pygame.font.Font("Lato-Black.ttf", 40)
game_over = font.render("Game Over", True, BLUE)

# Create classes for coins, enemies, and player car
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin_gold_racer.png")
        self.rect = self.image.get_rect()
        self.reset()  # Initialize coin position
        self.collect_sound = pygame.mixer.Sound('coins.mp3') 


    def reset(self):
        # Spawn the coin at a random position horizontally, above the screen
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), 0)
        self.rect.y = -self.rect.height  # coin position above the screen

    def move(self):
        # Move the coin downwards
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.reset()

    def coin_kill(self):
        # Randomly spawn the coin above the screen
        self.rect.center = (random.randint(0, SCREEN_WIDTH), 0)
    def play_collect_sound(self):
        self.collect_sound.play()  # Play the coins sound


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        # Reset enemy position if it goes beyond the screen boundaries
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# Sprites        
P1 = Player()
E1 = Enemy()

# sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
coins = pygame.sprite.Group()

INC_SPEED_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED_EVENT, 1000)  # Timer event to increase enemy speed

# randomly generate coins with different weights
def generate_coins():
    coin = Coin()
    COIN_VALUE = random.choices(COIN_WEIGHTS, weights=[weight / COIN_WEIGHT_TOTAL for weight in COIN_WEIGHTS])[0] * 50
   
    # Set COIN_VALUE based on a randomly chosen weight from COIN_WEIGHTS list,
    # then multiply it by 50 to determine the value of the coin.

    coins.add(coin)
    all_sprites.add(coin)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == INC_SPEED_EVENT:
            SPEED += 0.1  # Increase speed every second

    # Player movement
    P1.move()

    # Coin generation
    if random.random() < 0.003:  # Adjust probability as needed
        generate_coins()


    # Collision detection
    for coin in coins:
        if pygame.sprite.collide_rect(P1, coin):
            POINTS += 50
            coin.play_collect_sound()  # Play sound when the coins is collected
            coin.coin_kill()

    # Increase enemy speed when the player earns N coins
    if POINTS >= 500 * CYCLE:
        SPEED += 0.1
        CYCLE += 1

    # Drawing on screen
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(bg, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    point_counter = font_small.render(str(POINTS), True, BLUE)
    DISPLAYSURF.blit(point_counter, (SCREEN_WIDTH - point_counter.get_width() - 10, 10))

    # Moving and drawing sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Game over condition
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        last_point = font_small.render("Points: ", True, BLUE)
        DISPLAYSURF.blit(last_point, (40, 320))
        DISPLAYSURF.blit(point_counter, (200, 320))
        pygame.display.update()
        pygame.mixer.music.stop()
        pygame.time.wait(2000)  # Wait 2 seconds before exiting the game
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)