import pygame
import menu

pygame.init()

width, height = 900, 700
FPS = 40

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping-Pong")

clock = pygame.time.Clock()

def play_b():
    global menu_regim
    menu_regim = 1

def single_b():
    global menu_regim
    global player_regim
    play_b()
    player_regim = False

def double_b():
    global player_regim
    global menu_regim
    play_b()
    player_regim = True

def restart_b():
    global menu_regim
    menu_regim = 1
    platform0.center = start_coords[0]
    platform1.center = start_coords[1]
    ball.center = start_coords[2]

def main_menu_b():
    global menu_regim
    menu_regim = 0

platform0 = pygame.Rect(385, 650, 130, 30)
platform1 = pygame.Rect(385, 20, 130, 30)

ball = pygame.Rect(485, 285, 30, 30)

start_coords = (platform0.center, platform1.center, ball.center)

main_menu = menu.Menu(window, 'Ping-Pong', 100, (200, 0, 0), (0, 0, 200))
main_menu.add_button((400, 100), "Single", single_b, 75, (200, 0, 0), (0, 0, 200))
main_menu.add_button((400, 100), "Double", double_b, 75, (200, 0, 0), (0, 0, 200))

pause_menu = menu.Menu(window, 'Pause', 100, (200, 0, 0), (0, 0, 200))
pause_menu.add_button((400, 100), "Resume", play_b, 75, (200, 0, 0), (0, 0, 200))
pause_menu.add_button((400, 100), "Restart", restart_b, 75, (200, 0, 0), (0, 0, 200))
pause_menu.add_button((400, 100), "Main Menu", main_menu_b, 75, (200, 0, 0), (0, 0, 200))

winner_menu = menu.Menu(window, 'Winner', 100, (0, 0, 200), (200, 0, 0))
winner_menu.add_button((400, 100), "Restart", restart_b, 75, (0, 0, 200), (200, 0, 0))
winner_menu.add_button((400, 100), "Main Menu", main_menu_b, 75, (0, 0, 200), (200, 0, 0))

game_over_menu = menu.Menu(window, 'Winner', 100, (200, 0, 0), (0, 0, 200))
game_over_menu.add_button((400, 100), "Restart", restart_b, 75, (200, 0, 0), (0, 0, 200))
game_over_menu.add_button((400, 100), "Main Menu", main_menu_b, 75, (200, 0, 0), (0, 0, 200))

def run():
    global menu_regim
    global player_regim
    game = True
    step_bally = -5
    step_ballx = 5
    menu_regim = 0
    player_regim = False

    while game:
        if menu_regim == 0:
            main_menu.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in main_menu.BUTTONS:
                        if button[0].collidepoint(pygame.mouse.get_pos()):
                            button[-2]()
                            print(1)
            
        elif menu_regim == 1:
            window.fill((50, 50, 50))

            pygame.draw.rect(window, (200, 0, 0), platform0)
            pygame.draw.rect(window, (0, 0, 200), platform1)
            pygame.draw.circle(window, (0, 200, 0), ball.center, 15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu_regim = 2
                

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] and not platform0.right >= width:
                platform0.x += 5
            if keys[pygame.K_LEFT] and not platform0.left <= 0:
                platform0.x -= 5

            if player_regim:
                if keys[pygame.K_d] and not platform1.right >= width:
                    platform1.x += 5
                if keys[pygame.K_a] and not platform1.left <= 0:
                    platform1.x -= 5
            else:
                platform1.centerx = ball.centerx
            
            ball.y += step_bally
            ball.x += step_ballx

            if ball.colliderect(platform0) or ball.colliderect(platform1):
                step_bally = -step_bally
            if ball.left <= 0 or ball.right >= width:
                step_ballx = -step_ballx

            if ball.top <= 0:
                menu_regim = 3
            elif ball.bottom >= height:
                menu_regim = 4

        elif menu_regim == 2:
            pause_menu.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in pause_menu.BUTTONS:
                        if button[0].collidepoint(pygame.mouse.get_pos()):
                            button[-2]()
        
        elif menu_regim == 3:
            winner_menu.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in winner_menu.BUTTONS:
                        if button[0].collidepoint(pygame.mouse.get_pos()):
                            button[-2]()

        elif menu_regim == 4:
            game_over_menu.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in game_over_menu.BUTTONS:
                        if button[0].collidepoint(pygame.mouse.get_pos()):
                            button[-2]()

        pygame.display.flip()
        clock.tick(FPS)

run()
