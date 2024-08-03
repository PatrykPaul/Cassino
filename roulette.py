import sys
import pygame
import subprocess
from class_create_player import Player, PLAYER_SIZE_W, PLAYER_SIZE_H
from class_money_display import MoneyDisplay, BeltImage

python_path = sys.executable
roulette_script_path = "roulette_interface.py"
blackjack_script_path = "black_jack.py"

SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 768

TABLE_RECTS = [
    pygame.Rect(120, 80, 510, 250),
    pygame.Rect(800, 80, 510, 250),
    pygame.Rect(120, 430, 510, 250),
    pygame.Rect(830, 430, 510, 250)
]

button_image = pygame.image.load('buttons/przycisk.png')
enter_button_image = pygame.image.load('buttons/enter.png')

class ImageButton:
    def __init__(self, center_pos, image, scale=0.20):
        self.original_image = image
        scaled_width = int(self.original_image.get_width() * scale)
        scaled_height = int(self.original_image.get_height() * scale)
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(center=center_pos)
        self.visible = False

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

    def update_position(self, center_pos):
        self.rect.center = center_pos

class Roulette_Player(Player):
    def __init__(self, images, position=(700, 600), width=70, height=180):
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
        screen.blit(money_display, (15, 700))

    def draw_belt(self, screen):
        screen.blit(self.image, (-65, 635))

def ruletka():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Roulette Game Simulation')

    background_image = pygame.image.load('rooms/roulett.jpg')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    player_images = {
        'down': pygame.image.load('player/front.png'),
        'up': pygame.image.load('player/back.png'),
        'left': pygame.image.load('player/left.png'),
        'right': pygame.image.load('player/right.png')
    }
    for key in player_images:
        player_images[key] = pygame.transform.scale(player_images[key], (PLAYER_SIZE_W, PLAYER_SIZE_H))

    player = Roulette_Player(player_images)
    button = ImageButton((0, 0), button_image)

    # Inicjalizacja MoneyBeltDisplay
    FONT = pygame.font.Font(None, 36)
    money_belt_display = MoneyBeltDisplay(FONT, "money.txt", 'rooms/belt.png', 0.15)

    # Biały prostokąt na dole ekranu
    white_border_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 80, 150, 80)
    enter_button_rect = white_border_rect.inflate(-10, -10)  # zmniejszenie o 10px z każdej strony
    enter_button = ImageButton(enter_button_rect.center, enter_button_image, scale=0.13)

    # Load sounds
    background_sound = pygame.mixer.Sound('audio_files/casino_noise.mp3')
    footstep_sound = pygame.mixer.Sound('audio_files/foot_steps.mp3')

    background_sound.set_volume(0.8)
    footstep_sound.set_volume(0.8)

    background_sound.play(loops=-1)

    running = True
    clock = pygame.time.Clock()
    active_table = None
    launch_next_program = None

    while running:
        footstep_playing = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_rect = pygame.Rect(player.position[0], player.position[1], player.size[0], player.size[1])
                    if white_border_rect.colliderect(player_rect):
                        launch_next_program = "blackjack"
                        running = False
                    elif active_table:
                        launch_next_program = "roulette"
                        running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.move(keys)
            footstep_playing = True

        screen.blit(background_image, (0, 0))
        player.draw(screen)

        interaction = False
        for table_rect in TABLE_RECTS:
            if player.check_interaction([table_rect]):
                interaction = True
                button.update_position(table_rect.center)
                active_table = table_rect

        button.visible = interaction
        button.draw(screen)

        player_rect = pygame.Rect(player.position[0], player.position[1], player.size[0], player.size[1])
        enter_button.visible = white_border_rect.colliderect(player_rect)
        if enter_button.visible:
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
    ruletka()
