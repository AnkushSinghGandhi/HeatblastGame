import pygame
import random
import math
from pygame import mixer

# Calling Pygame init

pygame.init()

# Screen Creation

screen = pygame.display.set_mode((800, 600))

# Background

background = pygame.image.load('other_assets/background.png')

# Background Music

mixer.music.load('sounds/background.mp3')
mixer.music.play(-1)

play = 1

# fire blast

# hold - holding the fire
# blast - fireball is currently moving

fireball_img = pygame.image.load('assets/fireball.png')
fireball_y = 270
fireball_x = 10
fireball_y_change = 0
fireball_x_change = -10
fireball_state = 'hold'

# Game Over

over = pygame.font.Font('freesansbold.ttf', 40)

# score and life

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 19)

text_x = 7
text_y = 7

# Title and icon

pygame.display.set_caption('Heat-Blast @ankush_singh_gandhi')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# Player

player_img = pygame.image.load('assets/player.png')
player_y = 270
player_x = 10
player_y_change = 0

# Vilgax Drone

vilgax_drone_img = []
vilgax_drone_y = []
vilgax_drone_x = []
vilgax_drone_y_change = []
vilgax_drone_x_change = []
nums_of_drone = 6

for i in range(nums_of_drone):
    vilgax_drone_img.append(pygame.image.load('assets/drone.png'))
    vilgax_drone_y.append(random.randint(0, 599))
    vilgax_drone_x.append(random.randint(500, 730))
    vilgax_drone_y_change.append(3.3)
    vilgax_drone_x_change.append(-19)

# Gigantic Drone

gigantic_drone_img = pygame.image.load('assets/giganticdrone.png')
gigantic_drone_y = 270
gigantic_drone_x = 740
gigantic_drone_y_change = 3
gigantic_drone_x_change = 0
gigantic_drone_life = 10


def player(x, y):
    screen.blit(player_img, (x, y))


def drone(x, y, i):
    screen.blit(vilgax_drone_img[i], (x, y))


def giganticdrone(x, y):
    screen.blit(gigantic_drone_img, (x, y))


def fireblast(x, y):
    global fireball_state
    fireball_state = 'blast'
    screen.blit(fireball_img, (x + 10, y + 16))


def destruction(
    vilgax_drone_x,
    vilgax_drone_y,
    fireball_x,
    fireball_y,
    ):
    distance = math.sqrt(math.pow(vilgax_drone_x - fireball_x, 2)
                         + math.pow(vilgax_drone_y - fireball_y, 2))
    if distance < 39:
        return True
    else:
        return False


def gigantic_destruction(
    gigantic_drone_x,
    gigantic_drone_y,
    fireball_x,
    fireball_y,
    ):
    distance = math.sqrt(math.pow(gigantic_drone_x - fireball_x, 2)
                         + math.pow(gigantic_drone_y - fireball_y, 2))
    global gigantic_drone_life

    if gigantic_drone_life > 0:
        if distance < 39:
            gigantic_drone_life -= 1
            return True
        else:
            False


def show_score(x, y):
    score = font.render('Score : ' + str(score_value)
                        + ' MegaDrone life : '
                        + str(gigantic_drone_life), True, (255, 255,
                        255))
    screen.blit(score, (x, y))


def game_over(result):
    gover = over.render('Game Over' + result, True, (255, 255, 255))
    screen.blit(gover, (200, 250))


# Game Loop

running = True
while running:

    # RGB Value for screen

    screen.fill((0, 0, 0))

    # Background Image

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check wether is up or down

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_y_change += -7
            if event.key == pygame.K_DOWN:
                player_y_change += 7
            if event.key == pygame.K_SPACE:
                if fireball_state == 'hold':
                    fire_y = player_y
                    fireblast(player_x, player_y)
                    fire_sound = mixer.Sound('sounds/fire.wav')
                    fire_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0

    # Checking for boundries of Ben 10 aka our Player

    player_y += player_y_change

    if player_y <= 0:
        player_y = 0
    if player_y >= 530:
        player_y = 530

    # Checking for boundries of Drones
    # Vilgax Drone Movement

    for i in range(nums_of_drone):

        # Game Over
        if vilgax_drone_x[i] < 100:
            for j in range(nums_of_drone):
                gigantic_drone_x = 900
                gigantic_drone_y = 900
                vilgax_drone_y[j] = 900
            game_over(' You Lose')
            break

        
        vilgax_drone_y[i] += vilgax_drone_y_change[i]

        if vilgax_drone_y[i] <= 0:
            vilgax_drone_y_change[i] = 3.3
            vilgax_drone_x[i] += vilgax_drone_x_change[i]
        if vilgax_drone_y[i] >= 530:
            vilgax_drone_y_change[i] = -3.3
            vilgax_drone_x[i] += vilgax_drone_x_change[i]

        # Destruction

        drone_destruction = destruction(vilgax_drone_x[i],
                vilgax_drone_y[i], fireball_x, fireball_y)
        if drone_destruction:
            fireball_x = 10
            fireball_state = 'hold'
            score_value += 1
            vilgax_drone_y[i] = random.randint(0, 529)
            vilgax_drone_x[i] = random.randint(500, 730)
            explosion_sound = mixer.Sound('sounds/explosion.wav')
            explosion_sound.play()

        gigantic_drone_distruction = \
            gigantic_destruction(gigantic_drone_x, gigantic_drone_y,
                                 fireball_x, fireball_y)
        if gigantic_drone_distruction:
            fireball_x = 10
            fireball_state = 'hold'
            score_value += 5
        drone(vilgax_drone_x[i], vilgax_drone_y[i], i)
        if gigantic_drone_life == 0:
            gigantic_drone_x = 900
            gigantic_drone_y = 900
            vilgax_drone_y[i] = 900
            vilgax_drone_x[i] = 900
            game_over(' You Won')
            break


            if play <= 2:
                play += 1
                explosion_sound = mixer.Sound('sounds/Explosion.wav')
                explosion_sound.play()

        # Calling Drones

         

    # Checking for boundries of Gigantic Drones
    # Gigantic Drone Movement

    gigantic_drone_y += gigantic_drone_y_change

    if gigantic_drone_y <= 0:
        gigantic_drone_y_change = 3
    if gigantic_drone_y >= 530:
        gigantic_drone_y_change = -3

    # fireball Movement

    if fireball_x >= 800:
        fireball_state = 'hold'
        fireball_x = 10

    if fireball_state is 'blast':
        fireblast(fireball_x, fire_y)
        fireball_x -= fireball_x_change

    # Calling Gigantic drones

    giganticdrone(gigantic_drone_x, gigantic_drone_y)

    # Calling player

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
