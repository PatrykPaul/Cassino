import pygame
import subprocess
import sys
import time
from class_button_exit import Exit_Button

pygame.init()

python_path = sys.executable

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 515
BACKGROUND_COLOR = '#076128'
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra Startowa")

logo = pygame.image.load('buttons/bj.png')
logo = pygame.transform.scale(logo, (int(logo.get_width() * 0.3), int(logo.get_height() * 0.25)))

play_button = pygame.image.load('buttons/play.png')
play_button = pygame.transform.scale(play_button,
                                     (int(play_button.get_width() * 0.13), int(play_button.get_height() * 0.13)))

set_bet_button = pygame.image.load('buttons/set_bet.png')
set_bet_button = pygame.transform.scale(set_bet_button, (
    int(set_bet_button.get_width() * 0.13), int(set_bet_button.get_height() * 0.13)))

place_bet_button = pygame.image.load('buttons/place_bet.png')
place_bet_button = pygame.transform.scale(place_bet_button, (
    int(place_bet_button.get_width() * 0.13), int(place_bet_button.get_height() * 0.13)))

sound_image = pygame.image.load('buttons/sound.png')
sound_image = pygame.transform.scale(sound_image, (int(0.1 * SCREEN_WIDTH), int(0.1 * SCREEN_HEIGHT)))
x_sound_image = pygame.image.load('buttons/x_sound.png')
x_sound_image = pygame.transform.scale(x_sound_image, (int(0.1 * SCREEN_WIDTH), int(0.1 * SCREEN_HEIGHT)))

logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2, 90))
play_button_rect = play_button.get_rect(center=(SCREEN_WIDTH // 2, 240))
set_bet_button_rect = set_bet_button.get_rect(center=(SCREEN_WIDTH // 2, 345))
place_bet_button_rect = place_bet_button.get_rect(center=(SCREEN_WIDTH // 2, 425))
sound_button_rect = sound_image.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT))

button_sound = pygame.mixer.Sound('audio_files/button_press.mp3')

class MoneyDisplay:
    def __init__(self, font, money_file="money.txt"):
        self.font = font
        self.money_file = money_file
        self.money = self.read_money()

    def read_money(self):
        try:
            with open(self.money_file, "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def update_money(self):
        self.money = self.read_money()

class BeltImage:
    def __init__(self, belt_image_path, scale=1.0):
        self.image = pygame.image.load(belt_image_path)
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))

class MoneyBeltDisplay(MoneyDisplay, BeltImage):
    def __init__(self, font, money_file="money.txt", belt_image_path="belt.png", scale=1.0):
        MoneyDisplay.__init__(self, font, money_file)
        BeltImage.__init__(self, belt_image_path, scale)

    def draw_money(self, screen):
        money_display = self.font.render(f"{self.money}$", True, pygame.Color('black'))
        screen.blit(money_display, (15, 455))

    def draw_belt(self, screen):
        screen.blit(self.image, (-65, 390))

    def draw(self, screen):
        self.draw_belt(screen)
        self.draw_money(screen)

class ExitAndRunButton(Exit_Button):
    def handle_event(self, event, next_program):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                pygame.quit()
                subprocess.call([sys.executable, next_program])
                sys.exit()

final_bet = 0

def read_final_bet():
    try:
        with open("final_bet.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def run_black_jack():
    subprocess.call([python_path, 'black_jack_game.py'])

def run_black_jack_bet():
    subprocess.call([python_path, 'black_jack_bet.py'])

def update_current_bet():
    global final_bet
    final_bet = read_final_bet()

final_bet = read_final_bet()

pygame.mixer.music.load('audio_files/jazz.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

sound_on = True

def toggle_sound():
    global sound_on
    if sound_on:
        pygame.mixer.music.stop()
        sound_on = False
    else:
        pygame.mixer.music.play(-1)
        sound_on = True

font = pygame.font.Font(None, 36)
money_belt_display = MoneyBeltDisplay(font, "money.txt", "rooms/belt.png", 0.15)
exit_button = ExitAndRunButton(screen, "buttons/exit.png", (SCREEN_WIDTH, 0))  # Create ExitAndRunButton instance

running = True
last_money_update_time = time.time()

while running:
    current_time = time.time()

    if current_time - last_money_update_time > 3:
        money_belt_display.update_money()
        last_money_update_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            money_belt_display.update_money()
            if money_belt_display.money > 0:
                if play_button_rect.collidepoint(event.pos):
                    pygame.mixer.Sound.play(button_sound)
                    run_black_jack()
                elif set_bet_button_rect.collidepoint(event.pos):
                    pygame.mixer.Sound.play(button_sound)
                    run_black_jack_bet()
                elif place_bet_button_rect.collidepoint(event.pos):
                    pygame.mixer.Sound.play(button_sound)
                    update_current_bet()
            if sound_button_rect.collidepoint(event.pos):
                pygame.mixer.Sound.play(button_sound)
                toggle_sound()
        exit_button.handle_event(event, 'black_jack.py')

    screen.fill(pygame.Color(BACKGROUND_COLOR))
    screen.blit(logo, logo_rect)
    screen.blit(play_button, play_button_rect)
    screen.blit(set_bet_button, set_bet_button_rect)
    screen.blit(place_bet_button, place_bet_button_rect)

    if sound_on:
        screen.blit(sound_image, sound_button_rect)
    else:
        screen.blit(x_sound_image, sound_button_rect)

    if money_belt_display.money <= 0:
        final_bet = 0

    bet_text = font.render(f"current bet: {final_bet}", True, pygame.Color('black'), pygame.Color('white'))
    bet_rect = bet_text.get_rect(center=(SCREEN_WIDTH // 2, 485))
    screen.blit(bet_text, bet_rect)
    money_belt_display.draw(screen)
    exit_button.draw()

    pygame.display.flip()

pygame.quit()
