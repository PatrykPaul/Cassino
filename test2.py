import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 515
CARD_WIDTH, CARD_HEIGHT = 70, 100
FONT = pygame.font.Font(None, 36)

# Ustawienia ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Blackjack')


# Ładowanie tła
def load_background(image_path):
    background = pygame.image.load(image_path)
    # background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return background


def load_card_images(deck):
    card_images = {}
    for card_path in deck:
        image = pygame.image.load(card_path)
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        card_images[card_path] = image
    # Dodajemy obrazek rewersu karty
    back_image = pygame.image.load('cards/back.PNG')
    back_image = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))
    card_images['cards/back.PNG'] = back_image
    return card_images


def shuffle_deck(deck):
    shuffled_deck = deck[:]
    random.shuffle(shuffled_deck)
    return shuffled_deck


def card_value(card_path):
    rank = card_path.split('/')[2].split('.')[0]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'AS':
        return 11
    else:
        return int(rank)


def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if 'AS' in card)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


def draw_cards(screen, card_images, card_paths, x_start, y):
    card_spacing = 20  # Odstępy między kartami
    total_width = len(card_paths) * (CARD_WIDTH + card_spacing) - card_spacing
    start_x = x_start - total_width // 2  # Wyśrodkowanie kart

    for i, card in enumerate(card_paths):
        screen.blit(card_images[card], (start_x + i * (CARD_WIDTH + card_spacing), y))


def draw_text(screen, text, x, y):
    # Render the text
    text_surface = FONT.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x, y))

    # Define the background rectangle
    background_rect = text_rect.inflate(20, 10)  # Increase the size of the background rectangle

    # Draw the background rectangle
    pygame.draw.rect(screen, (255, 255, 255), background_rect)

    # Draw the text on top of the background
    screen.blit(text_surface, text_rect)



def reset_game(deck_of_cards):
    shuffled_deck = shuffle_deck(deck_of_cards)
    player_hand = [shuffled_deck.pop() for _ in range(2)]
    dealer_hand = [shuffled_deck.pop() for _ in range(2)]
    return shuffled_deck, player_hand, dealer_hand


# Ścieżka do obrazka tła
background_image = 'table.PNG'
background = load_background(background_image)

# Twoja talia kart
deck_of_cards = [
    'cards/karo/AS.PNG', 'cards/karo/2.PNG', 'cards/karo/3.PNG', 'cards/karo/4.PNG', 'cards/karo/5.PNG',
    'cards/karo/6.PNG',
    'cards/karo/7.PNG', 'cards/karo/8.PNG', 'cards/karo/9.PNG', 'cards/karo/10.PNG', 'cards/karo/J.PNG',
    'cards/karo/Q.PNG', 'cards/karo/K.PNG',
    'cards/pik/AS.PNG', 'cards/pik/2.PNG', 'cards/pik/3.PNG', 'cards/pik/4.PNG', 'cards/pik/5.PNG', 'cards/pik/6.PNG',
    'cards/pik/7.PNG', 'cards/pik/8.PNG', 'cards/pik/9.PNG', 'cards/pik/10.PNG', 'cards/pik/J.PNG', 'cards/pik/Q.PNG',
    'cards/pik/K.PNG',
    'cards/kier/AS.PNG', 'cards/kier/2.PNG', 'cards/kier/3.PNG', 'cards/kier/4.PNG', 'cards/kier/5.PNG',
    'cards/kier/6.PNG',
    'cards/kier/7.PNG', 'cards/kier/8.PNG', 'cards/kier/9.PNG', 'cards/kier/10.PNG', 'cards/kier/J.PNG',
    'cards/kier/Q.PNG', 'cards/kier/K.PNG',
    'cards/trefl/AS.PNG', 'cards/trefl/2.PNG', 'cards/trefl/3.PNG', 'cards/trefl/4.PNG', 'cards/trefl/5.PNG',
    'cards/trefl/6.PNG',
    'cards/trefl/7.PNG', 'cards/trefl/8.PNG', 'cards/trefl/9.PNG', 'cards/trefl/10.PNG', 'cards/trefl/J.PNG',
    'cards/trefl/Q.PNG', 'cards/trefl/K.PNG'
]

# Załadowanie obrazków kart
card_images = load_card_images(deck_of_cards)
shuffled_deck, player_hand, dealer_hand = reset_game(deck_of_cards)

# Załadowanie przycisku z pytaniem
button_image = pygame.image.load('question.png')
button_image = pygame.transform.scale(button_image, (100, 50))  # Możesz dostosować rozmiar
button_rect = button_image.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))


game_over = False
player_turn = True
display_text = False

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):  # Sprawdzenie, czy kliknięto w przycisk
                display_text = not display_text  # Zmiana stanu wyświetlania tekstu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h and player_turn and not game_over:  # Hit
                player_hand.append(shuffled_deck.pop())
                if hand_value(player_hand) > 21:
                    game_over = True
                    player_turn = False
            elif event.key == pygame.K_s and not game_over:  # Stand
                player_turn = False
                while hand_value(dealer_hand) < 17:
                    dealer_hand.append(shuffled_deck.pop())
                game_over = True
            elif event.key == pygame.K_r and game_over:  # Restart
                shuffled_deck, player_hand, dealer_hand = reset_game(deck_of_cards)
                game_over = False
                player_turn = True

    screen.blit(background, (0, 0))  # Czyszczenie ekranu przez narysowanie tła

    # Wyśrodkowanie kart gracza i krupiera
    draw_cards(screen, card_images, player_hand, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    draw_cards(screen, card_images, dealer_hand, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

    if game_over:
        dealer_score = hand_value(dealer_hand)
        player_score = hand_value(player_hand)
        if player_score > 21:
            result = "Player busts! You lose."
        elif dealer_score > 21 or player_score > dealer_score:
            result = "Player wins!"
        elif player_score < dealer_score:
            result = "Dealer wins!"
        else:
            result = "Push! It's a tie."
        # Wyświetlanie wyniku w środku ekranu
        draw_text(screen, result, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    if not game_over:
        # Wyświetlanie komend
        draw_text(screen, 'H for hit, S for stand, R to restart', 440, 315)
    if display_text:
        # Rysowanie białego prostokąta
        pygame.draw.rect(screen, (255, 255, 255), (100, 100, 400, 100))
        # Możesz dodać wyświetlanie tekstu tu, jeśli chcesz, żeby był od razu widoczny

    # Rysowanie przycisku (zawsze na wierzchu)
    screen.blit(button_image, button_rect)

    pygame.display.update()

pygame.quit()
