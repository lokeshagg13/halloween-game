"""
This is a python game module
"""

import random
import pygame

pygame.init()

#######################################

# Colors

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (55, 55, 55)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Fonts

label_font = pygame.font.Font('assets\\fonts\\Plaguard-ZVnjx.otf', 80)
medium_font = pygame.font.Font('assets\\fonts\\Plaguard-ZVnjx.otf', 40)
small_font = pygame.font.Font('assets\\fonts\\Roboto-Bold.ttf', 20)

#########################

# Game parameters

GAME_TITLE = 'Noble vs Evil'

trick_treat_drop_counter = 0
game_score = 0
game_score_lims = {"min": -4, "max": 4}
trick_bag = []
treat_bag = []

#########################

# Initialise game screen

infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h - 50

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(GAME_TITLE)

########################

# Game elements orientation and coordinates
game_panel_coords = (0, 0)
game_panel_dims = (WIDTH, 600)
game_panel_left_x = game_panel_coords[0]
game_panel_right_x = game_panel_coords[0] + game_panel_dims[0]
witch_coords = (725, 255)
witch_dims = (100, 175)
container_coords = (10, 450)
container_dims = (100, 150)
trick_treat_coords = (0, 0)
trick_treat_dims = {'treat_1': (50, 50), 'treat_2': (50, 50), 'treat_3': (50, 50), 'treat_4': (50, 25), 'treat_5': (50, 50),
                     'treat_6': (50, 75), 'trick_1': (50, 50), 'trick_2': (50, 50), 'trick_3': (50, 30), 'trick_4': (50, 50), 'trick_5': (75, 50), 'trick_6': (50, 75)}
trick_treat_limit_y = container_coords[1] + container_dims[1] / 2


#########################

# Game Methods

def create_witch(witch_score):
    witch_loc = 'assets/images/'
    if witch_score > 4:
        witch_code = 'good_4'
    elif 0 < witch_score <= 4:
        witch_code = f'good_{witch_score}'
    elif -3 <= witch_score <= 0:
        witch_code = f'bad_{abs(witch_score) + 1}'
    else:
        witch_code = 'burst'
    witch = pygame.image.load(witch_loc + witch_code + '.png')
    witch = pygame.transform.scale(witch, (witch_dims[0], witch_dims[1]))
    witch_rect = witch.get_rect()
    witch_rect.top = witch_coords[1]
    witch_rect.left = witch_coords[0]
    return witch, witch_rect


def create_container():
    container = pygame.image.load('assets/images/container.png')
    container = pygame.transform.scale(container, (container_dims[0], container_dims[1]))
    container_rect = container.get_rect()
    container_rect.top = container_coords[1]
    container_rect.left = container_coords[0]
    return container, container_rect


def create_trick_or_treat():
    bias_measure = 0.5
    trick_or_treat = random.random()
    trick_treat_loc = 'assets/images/trick_or_treat/'
    trick_or_treat_num = random.randint(1, 5)
    trick_treat_coords = (random.randint(game_panel_left_x + 50, game_panel_right_x - 50), 20)
    trick_treat_speed = 3 * (game_score + 1) + 5
    if trick_or_treat < bias_measure:
        name = f'treat_{trick_or_treat_num}'
        dims = trick_treat_dims[name]
        treat = pygame.image.load(f'{trick_treat_loc}{name}.png')
        treat = pygame.transform.scale(treat, (dims[0], dims[1]))
        treat_rect = treat.get_rect()
        treat_rect.x = trick_treat_coords[0]
        treat_rect.y = trick_treat_coords[1]
        treat_bag.append((treat, treat_rect, trick_treat_speed))
    else:
        name = f'trick_{trick_or_treat_num}'
        dims = trick_treat_dims[name]
        trick = pygame.image.load(f'{trick_treat_loc}{name}.png')
        trick = pygame.transform.scale(trick, (dims[0], dims[1]))
        trick_rect = trick.get_rect()
        trick_rect.x = trick_treat_coords[0]
        trick_rect.y = trick_treat_coords[1]
        trick_bag.append((trick, trick_rect, trick_treat_speed))


def check_inbound_rect(outer_rect, inner_rect):
    if outer_rect.top <= inner_rect.top and outer_rect.bottom >= inner_rect.bottom and outer_rect.left <= inner_rect.left and outer_rect.right >= inner_rect.right:
        return True
    return False


def move_tricks_and_treats(container_rect):
    global game_score
    wasted_tricks_idx = []
    wasted_treats_idx = []
    for idx, (trick, trick_rect, trick_speed) in enumerate(trick_bag):
        if trick_rect.top + trick_speed < trick_treat_limit_y:
            trick_rect.top += trick_speed
        else:
            wasted_tricks_idx.append(idx)
            if check_inbound_rect(container_rect, trick_rect) and game_score > game_score_lims["min"]:
                game_score -= 1
    for idx in wasted_tricks_idx:
        del trick_bag[idx]

    for idx, (treat, treat_rect, treat_speed) in enumerate(treat_bag):
        if treat_rect.top + treat_speed < trick_treat_limit_y:
            treat_rect.top += treat_speed
        else:
            wasted_treats_idx.append(idx)
            if check_inbound_rect(container_rect, treat_rect) and game_score < game_score_lims["max"]:
                game_score += 1
    for idx in wasted_treats_idx:
        del treat_bag[idx]


def check_tricks_and_treats(container_rect):
    global game_score
    for trick, trick_rect, trick_speed in trick_bag:
        if check_inbound_rect(container_rect, trick_rect) and game_score > game_score_lims["min"]:
            game_score -= 1
    for treat, treat_rect, treat_speed in trick_bag:
        if check_inbound_rect(container_rect, treat_rect) and game_score < game_score_lims["max"]:
            game_score += 1


##########################

# Game Loop

FPS = 60
timer = pygame.time.Clock()
bg_img = pygame.image.load('assets/images/background.jpg').convert()
bg_img.set_alpha(75)
bg_img = pygame.transform.scale(bg_img, (game_panel_dims[0], game_panel_dims[1]))
container, container_rect = create_container()

RUN = True
while RUN:
    timer.tick(60)
    screen.fill(black)
    pygame.draw.rect(screen, gray, [
        game_panel_coords[0], game_panel_coords[1], game_panel_dims[0], game_panel_dims[1]], 1, 5)
    screen.blit(bg_img, (game_panel_coords[0], game_panel_coords[1]))
    witch, witch_rect = create_witch(game_score)
    screen.blit(witch, witch_rect)
    for trick, trick_rect, trick_speed in trick_bag:
        screen.blit(trick, trick_rect)
    for treat, treat_rect, treat_speed in treat_bag:
        screen.blit(treat, treat_rect)
    check_tricks_and_treats(container_rect)
    cursor_position = pygame.mouse.get_pos()
    if cursor_position[0] <= game_panel_left_x:
        container_rect.left = game_panel_left_x
    elif game_panel_left_x <= cursor_position[0] <= game_panel_right_x - 150:
        container_rect.left = cursor_position[0] - 50
    elif cursor_position[0] >= game_panel_right_x - 150:
        container_rect.left = game_panel_right_x - 150
    screen.blit(container, container_rect)

    if trick_treat_drop_counter % 20 == 0:
        create_trick_or_treat()
    move_tricks_and_treats(container_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    trick_treat_drop_counter += 1
    pygame.display.flip()

pygame.quit()
