import pygame
import random

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

########################

# Game elements orientation and coordinates

button_dims = (150, 50)
game_panel_coords = (350, 100)
game_panel_dims = (600, 500)
game_panel_top_y = game_panel_coords[1]
game_panel_bottom_y = game_panel_coords[1] + game_panel_dims[1]
game_title_coords = (500, 30)
won_title_coords = (600, 250)
missed_text_coords = (500, 300)
restart_button_coords = (460, 350)
restart_button_text_coords = (500, 360)
quit_button_coords = (660, 350)
quit_button_text_coords = (710, 360)

#########################

# Game parameters

game_title = 'Shoot It'
balloon_speed = 2
gun_speed = 5
bullet_speed = balloon_speed * 10
max_bullets = 10
number_missed_shots = 0
bullets = []


#########################

# Game Methods

def create_balloon():
    balloon = pygame.image.load('assets\\images\\balloon.gif')
    balloon = pygame.transform.scale(balloon, (40, 80))
    balloon_rect = balloon.get_rect()
    balloon_rect.top = game_panel_top_y
    balloon_rect.left = game_panel_coords[0] + 10
    return (balloon, balloon_rect)


def create_fused_balloon(last_balloon_y):
    fused = pygame.image.load('assets\\images\\burst.png')
    fused = pygame.transform.scale(fused, (40, 40))
    fused_rect = fused.get_rect()
    fused_rect.top = last_balloon_y
    fused_rect.left = game_panel_coords[0] + 10
    return (fused, fused_rect)


def create_gun():
    gun = pygame.image.load('assets\\images\\gun.png')
    gun = pygame.transform.scale(gun, (80, 60))
    gun_rect = gun.get_rect()
    gun_rect.top = game_panel_top_y
    gun_rect.right = game_panel_coords[0] + game_panel_dims[0] - 10
    return (gun, gun_rect)


def create_bullet(x, y):
    bullet = pygame.image.load('assets\\images\\bullet.png')
    bullet = pygame.transform.scale(bullet, (50, 25))
    bullet_rect = bullet.get_rect()
    bullet_rect.top = y
    bullet_rect.right = x
    bullets.append((bullet, bullet_rect))
    return (bullet, bullet_rect)


def move_all_bullets():
    for bullet_info in bullets:
        bullet_rect = bullet_info[1]
        if bullet_rect.left > balloon_rect.right:
            bullet_rect.left -= bullet_speed


def check_bullet_position():
    global number_missed_shots
    wasted_bullets_idx = []
    for bullet_idx, bullet_info in enumerate(bullets):
        bullet_rect = bullet_info[1]
        if bullet_rect.left <= balloon_rect.right + 5:
            if bullet_rect.top >= balloon_rect.top - 5 and bullet_rect.bottom <= balloon_rect.bottom + 5:
                return "WON"
            else:
                wasted_bullets_idx.append(bullet_idx)
    for idx in wasted_bullets_idx:
        del bullets[idx]
        number_missed_shots = number_missed_shots + 1
    return "RUNNING"


def create_button_template():
    button_rect = pygame.Rect(0, 0, button_dims[0], button_dims[1])
    return button_rect


#########################

# Initialise game environment

infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h - 50

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(game_title)

balloon, balloon_rect = create_balloon()
gun, gun_rect = create_gun()
restart_button_rect = create_button_template()
restart_button_rect.left, restart_button_rect.top = restart_button_coords[0], restart_button_coords[1]
quit_button_rect = create_button_template()
quit_button_rect.left, quit_button_rect.top = quit_button_coords[0], quit_button_coords[1]

##########################

# Game Loop

fps = 60
timer = pygame.time.Clock()

run = True
while run:
    timer.tick(60)
    screen.fill(black)
    move_all_bullets()
    status = check_bullet_position()
    game_title = label_font.render('SHOOT IT', True, white)
    screen.blit(game_title, (game_title_coords[0], game_title_coords[1]))

    pygame.draw.rect(screen, gray,
                     [game_panel_coords[0], game_panel_coords[1], game_panel_dims[0], game_panel_dims[1]],
                     1, 5)

    screen.blit(gun, gun_rect)

    if status == 'WON':
        fused, fused_rect = create_fused_balloon(balloon_rect.top)
        screen.blit(fused, fused_rect)

        won_title = medium_font.render('WON', True, white)
        screen.blit(won_title, (won_title_coords[0], won_title_coords[1]))

        missed_text = small_font.render(f'Number of missed shots: {number_missed_shots}', True, white)
        screen.blit(missed_text, (missed_text_coords[0], missed_text_coords[1]))

        pygame.draw.rect(screen, white, restart_button_rect, width=1, border_radius=5)
        restart_button_title = small_font.render('Restart', True, white)
        screen.blit(restart_button_title, (restart_button_text_coords[0], restart_button_text_coords[1]))

        pygame.draw.rect(screen, white, quit_button_rect, width=1, border_radius=5)
        quit_button_title = small_font.render('Quit', True, white)
        screen.blit(quit_button_title, (quit_button_text_coords[0], quit_button_text_coords[1]))



    else:
        if balloon_rect.top < game_panel_top_y or balloon_rect.bottom > game_panel_bottom_y:
            balloon_speed = -balloon_speed
        else:
            choices = [1] * 100
            choices.append(-1)
            balloon_speed = balloon_speed * random.choice(choices)
        balloon_rect.update(
            [balloon_rect.left, balloon_rect.top + balloon_speed, balloon_rect.width, balloon_rect.height])
        screen.blit(balloon, balloon_rect)

        for (bullet, bullet_rect) in bullets:
            screen.blit(bullet, bullet_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and status == 'WON':
            if restart_button_rect.collidepoint(event.pos):
                status = 'RUNNING'
                bullets = []
                number_missed_shots = 0
                continue
            elif quit_button_rect.collidepoint(event.pos):
                run = False

        elif event.type == pygame.KEYDOWN and status != 'WON':
            if event.key == pygame.K_SPACE and len(bullets) < 10:
                create_bullet(gun_rect.left, (gun_rect.top + gun_rect.bottom) / 2)

    keys = pygame.key.get_pressed()
    if status != 'WON' and (keys[pygame.K_DOWN] or keys[pygame.K_s]) and gun_rect.bottom < game_panel_bottom_y:
        gun_rect.top += gun_speed
    elif status != 'WON' and (keys[pygame.K_UP] or keys[pygame.K_w]) and gun_rect.top > game_panel_top_y:
        gun_rect.top -= gun_speed

    pygame.display.flip()

pygame.quit()
