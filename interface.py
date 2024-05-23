# interface.py
import pygame

def load_scaled_image(path, scale):
    image = pygame.image.load(path)
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    return pygame.transform.scale(image, (width, height))

class Button:
    def __init__(self, image_path, scale, bet, position):
        self.image = load_scaled_image(image_path, scale)
        self.rect = self.image.get_rect(topleft=position)
        self.bet = bet

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Interface:
    def __init__(self, font):
        self.font = font
        self.buttons = [
            Button('buttons/100.png', 0.08, 100, (170, 621)),
            Button('buttons/1000.png', 0.08, 1000, (240, 621)),
            Button('buttons/10000.png', 0.08, 10000, (310, 621)),
            Button('buttons/ALL-IN.png', 0.08, 'all-in', (380, 621)),
            Button('buttons/clear.png', 0.08, 'clear', (450, 621))
        ]
        self.current_bet = 0
        self.result_text = ""
        self.message_text = ""
        self.result_color = pygame.Color('white')
        self.message_color = None
        self.total_win_amount = 0

    def draw_buttons(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def draw_text(self, screen):
        bet_display = self.font.render(f"Current Bet: ${self.current_bet}", True, (255, 255, 255))
        screen.blit(bet_display, (450, 580))
        if self.result_text:
            result_surface = self.font.render(self.result_text, True, self.result_color)
            screen.blit(result_surface, (600, 250))
        if self.message_text:
            message_surface = self.font.render(self.message_text, True, self.message_color)
            screen.blit(message_surface, (600, 300))
            if self.total_win_amount > 0:
                win_amount_text = f"Won: ${self.total_win_amount}"
                win_amount_surface = self.font.render(win_amount_text, True, self.message_color)
                screen.blit(win_amount_surface, (600, 350))

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_clicked(pos):
                return button.bet
        return None

    def reset_bet(self):
        self.current_bet = 0

    def add_bet(self, amount):
        self.current_bet += amount

    def set_result(self, result_text, message_text, message_color, total_win_amount=0):
        self.result_text = result_text
        self.message_text = message_text
        self.message_color = message_color
        self.total_win_amount = total_win_amount
