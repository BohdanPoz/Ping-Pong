import pygame
import menu

pygame.init()

WIDTH, HEIGHT = 900, 700
FPS = 40

window = pygame.display.set_mode((WIDTH, HEIGHT))
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
    platform0.center = start_coords[0]
    platform1.center = start_coords[1]
    ball.center = start_coords[2]

def double_b():
    global player_regim
    global menu_regim
    play_b()
    player_regim = True
    platform0.center = start_coords[0]
    platform1.center = start_coords[1]
    ball.center = start_coords[2]

def restart_b():
    global menu_regim
    menu_regim = 1
    platform0.center = start_coords[0]
    platform1.center = start_coords[1]
    ball.center = start_coords[2]

def main_menu_b():
    global menu_regim
    menu_regim = 0

class Platform(pygame.Rect):
    def __init__(self, x, y, width, height, step, color, control='player0'):
        super().__init__(x, y, width, height)

        self.COLOR = color
        self.CONTROL = control
        self.STEP = step

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, self)

    def move(self, ball):
        if 'player' in self.CONTROL:
            if self.CONTROL[-1] == '0':
                control_keys = (pygame.K_RIGHT, pygame.K_LEFT)
            else:
                control_keys = (pygame.K_d, pygame.K_a)
            keys = pygame.key.get_pressed()

            if keys[control_keys[0]] and not self.right >= WIDTH:
                self.x += self.STEP
            if keys[control_keys[1]] and not self.left <= 0:
                self.x -= self.STEP
        elif self.CONTROL == 'computor':
            self.centerx = ball.centerx

platform0 = Platform(WIDTH//2-130//2, HEIGHT-40, 130, 30, 5, (200, 0, 0))
platform1 = Platform(WIDTH//2-130//2, 20, 130, 30, 5, (0, 0, 200), 'computor')

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
        if not player_regim and platform1.CONTROL != 'computor':
            platform1.CONTROL = 'computor'
        elif player_regim and platform1.CONTROL != 'player1':
            platform1.CONTROL = 'player1'

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

            platform0.draw(window)
            platform1.draw(window)
            pygame.draw.circle(window, (0, 200, 0), ball.center, 15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu_regim = 2

            platform0.move(ball)
            platform1.move(ball)
            
            ball.y += step_bally
            ball.x += step_ballx

            if ball.colliderect(platform0) or ball.colliderect(platform1):
                step_bally = -step_bally
            if ball.left <= 0 or ball.right >= WIDTH:
                step_ballx = -step_ballx

            if ball.top <= 0:
                menu_regim = 3
            elif ball.bottom >= HEIGHT:
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
