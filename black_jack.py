import sys
import pygame
import subprocess
from class_create_player import Player
from class_money_display import MoneyDisplay, BeltImage

python_path = sys.executable
blackjack_script_path = "black_jack_interface.py"
roulette_script_path = "roulette.py"

pygame.init()

background_sound = pygame.mixer.Sound('audio_files/casino_noise.mp3')
footstep_sound = pygame.mixer.Sound('audio_files/foot_steps.mp3')

background_sound.set_volume(0.8)
footstep_sound.set_volume(0.8)

background_sound.play(loops=-1)

SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 768

TABLE_INTERACTION_RECTS = [
    pygame.Rect(830, 580, 230, 130),
    pygame.Rect(485, 225, 160, 85),
    pygame.Rect(840, 225, 160, 85),
    pygame.Rect(965, 370, 200, 110),
    pygame.Rect(650, 370, 200, 110),
    pygame.Rect(310, 370, 200, 110),
    pygame.Rect(410, 580, 230, 130)
]

button_image = pygame.image.load('buttons/przycisk.png')
enter_button_image = pygame.image.load('buttons/enter.png')

class ImageButton:
    def __init__(self, center_pos, image, target_rect, scale=1.0):
        self.original_image = image
        scale_width = target_rect.width / self.original_image.get_width()
        scale_height = target_rect.height / self.original_image.get_height()
        scale = min(scale_width, scale_height) * scale
        width = int(self.original_image.get_width() * scale)
        height = int(self.original_image.get_height() * scale)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect(center=center_pos)
        self.highlighted = False

    def draw(self, screen):
        if self.highlighted:
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)

class Black_Jack_Player(Player):
    def __init__(self, images, position=(700, 600), width=60, height=160):
        super().__init__(images, position)
        self.size = (width, height)
        self.speed = 5
        self.resize_images()

    def resize_images(self):
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], self.size)

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.position = (self.position[0], max(0, self.position[1] - self.speed))
        if keys[pygame.K_DOWN]:
            self.position = (self.position[0], min(SCREEN_HEIGHT - self.size[1], self.position[1] + self.speed))
        if keys[pygame.K_LEFT]:
            self.position = (max(0, self.position[0] - self.speed), self.position[1])
        if keys[pygame.K_RIGHT]:
            self.position = (min(SCREEN_WIDTH - self.size[0], self.position[0] + self.speed), self.position[1])

class MoneyBeltDisplay(MoneyDisplay, BeltImage):
    def __init__(self, font, money_file_path, belt_image_path, belt_scale):
        MoneyDisplay.__init__(self, font, money_file_path)
        BeltImage.__init__(self, belt_image_path, belt_scale)

    def draw(self, screen):
        self.draw_belt(screen)
        self.draw_money(screen)

    def draw_money(self, screen):
        money_display = self.font.render(f"{self.money}$", True, pygame.Color('black'))
        screen.blit(money_display, (15, 700))  # Adjusted position to fit within screen height

    def draw_belt(self, screen):
        screen.blit(self.image, (-65, 635))

def game_loop():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Casino Game Simulation')

    background_image = pygame.image.load('rooms/blackjack.jpg')
    player_images = {
        'down': pygame.image.load('player/front.png'),
        'up': pygame.image.load('player/back.png'),
        'left': pygame.image.load('player/left.png'),
        'right': pygame.image.load('player/right.png')
    }

    player = Black_Jack_Player(player_images)
    buttons = [ImageButton(rect.center, button_image, rect) for rect in TABLE_INTERACTION_RECTS]

    FONT = pygame.font.Font(None, 36)
    money_belt_display = MoneyBeltDisplay(FONT, "money.txt", 'rooms/belt.png', 0.15)

    white_border_rect = pygame.Rect(SCREEN_WIDTH // 2 - 30, 50, 100, 180)
    enter_button_rect = white_border_rect.inflate(-20, -20)
    enter_button = ImageButton(enter_button_rect.center, enter_button_image, enter_button_rect, scale=1.2)

    clock = pygame.time.Clock()
    running = True
    interact_rect = None
    launch_next_program = False

    while running:
        footstep_playing = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_rect = pygame.Rect(player.position[0], player.position[1], player.size[0], player.size[1])
                    if white_border_rect.colliderect(player_rect):
                        launch_next_program = "roulette"
                        running = False
                    elif interact_rect:
                        for button in buttons:
                            if button.rect.colliderect(interact_rect):
                                launch_next_program = "blackjack"
                                running = False
                                break

        if not running:
            break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.move(keys)
            footstep_playing = True

        player_rect = pygame.Rect(player.position[0], player.position[1], player.size[0], player.size[1])

        screen.blit(background_image, (0, 0))
        player.draw(screen)

        interact_rect = None
        for rect in TABLE_INTERACTION_RECTS:
            if rect.colliderect(player_rect):
                interact_rect = rect
                break

        for button in buttons:
            button.highlighted = button.rect.colliderect(interact_rect) if interact_rect else False
            if button.highlighted:
                button.draw(screen)

        enter_button.highlighted = white_border_rect.colliderect(player_rect)
        if enter_button.highlighted:
            enter_button.draw(screen)

        if footstep_playing:
            if not footstep_sound.get_num_channels():
                footstep_sound.play()
        else:
            footstep_sound.stop()

        money_belt_display.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

    if launch_next_program == "roulette":
        subprocess.call([python_path, roulette_script_path])
    elif launch_next_program == "blackjack":
        subprocess.call([python_path, blackjack_script_path])

if __name__ == '__main__':
    game_loop()
