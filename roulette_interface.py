import pygame
import subprocess
import sys
import time
from class_button_exit import Exit_Button
from class_question import QuestionButton

pygame.init()

python_path = sys.executable

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 515
BACKGROUND_COLOR = "#016600"
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra Startowa")

logo = pygame.image.load('buttons/roulette.png')
logo = pygame.transform.scale(logo, (int(logo.get_width() * 0.3), int(logo.get_height() * 0.25)))

play_button = pygame.image.load('buttons/play.png')
play_button = pygame.transform.scale(play_button, (int(play_button.get_width() * 0.13), int(play_button.get_height() * 0.13)))

sound_image = pygame.image.load('buttons/sound.png')
sound_image = pygame.transform.scale(sound_image, (int(0.1 * SCREEN_WIDTH), int(0.1 * SCREEN_HEIGHT)))
x_sound_image = pygame.image.load('buttons/x_sound.png')
x_sound_image = pygame.transform.scale(x_sound_image, (int(0.1 * SCREEN_WIDTH), int(0.1 * SCREEN_HEIGHT)))

logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2, 100))
play_button_rect = play_button.get_rect(center=(SCREEN_WIDTH // 2, 270))
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

class BlackjackQuestionButton(QuestionButton):
    def __init__(self, image_path, position, size, font):
        super().__init__(image_path, position, size)
        self.font = font

    def draw_text(self, screen):
        if self.display_text:
            pygame.draw.rect(screen, (255, 255, 255), (150, 100, 650, 300))
            self._draw_text(screen, "In this game, you place bets on numbers,colors,", 470, 160, self.font)
            self._draw_text(screen, "or groups of numbers on the table.", 390, 190, self.font)
            self._draw_text(screen, "Click the Spin button to spin the wheel,", 420, 220, self.font)
            self._draw_text(screen, "which randomly selects a number.", 390, 250, self.font)
            self._draw_text(screen, "You win if the spin result matches your bet,.", 445, 280, self.font)
            self._draw_text(screen, "and the amount you win depends", 385, 310, self.font)
            self._draw_text(screen, "on the type of bet you placed.", 360, 340, self.font)

def run_roulette():
    subprocess.call([python_path, 'roulette_game.py'])

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
exit_button = ExitAndRunButton(screen, "buttons/exit.png", (100, -10))
question_button = BlackjackQuestionButton('buttons/question.png', (SCREEN_WIDTH , 75), (70, 60), font)

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
                    run_roulette()
            if sound_button_rect.collidepoint(event.pos):
                pygame.mixer.Sound.play(button_sound)
                toggle_sound()
        question_button.handle_event(event)
        exit_button.handle_event(event, 'roulette.py')

    screen.fill(pygame.Color(BACKGROUND_COLOR))
    screen.blit(logo, logo_rect)
    screen.blit(play_button, play_button_rect)

    if sound_on:
        screen.blit(sound_image, sound_button_rect)
    else:
        screen.blit(x_sound_image, sound_button_rect)

    question_button.draw(screen)
    money_belt_display.draw(screen)
    exit_button.draw()
    question_button.draw_text(screen)

    pygame.display.flip()

pygame.quit()
