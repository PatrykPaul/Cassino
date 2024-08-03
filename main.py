import pygame
import sys
import subprocess

pygame.init()
pygame.mixer.init()
python_path = sys.executable
button_sound = pygame.mixer.Sound("audio_files/button_press.mp3")

background = pygame.image.load("rooms/main.png")
play_button_image = pygame.image.load("buttons/play.png")
exchange_button_image = pygame.image.load("buttons/exchange.png")

background = pygame.transform.scale(background, (int(background.get_width() * 0.7), int(background.get_height() * 0.7)))
new_width, new_height = background.get_width(), background.get_height()

screen = pygame.display.set_mode((new_width, new_height))
pygame.display.set_caption("Aplikacja Pygame")

play_button_image = pygame.transform.scale(play_button_image, (int(play_button_image.get_width() * 0.13), int(play_button_image.get_height() * 0.13)))
exchange_button_image = pygame.transform.scale(exchange_button_image, (int(exchange_button_image.get_width() * 0.13), int(exchange_button_image.get_height() * 0.13)))

play_button_rect = play_button_image.get_rect()
play_button_rect.topleft = (screen.get_width() // 2 - play_button_rect.width // 2, 470)

exchange_button_rect = exchange_button_image.get_rect()
exchange_button_rect.topleft = (screen.get_width() // 2 - exchange_button_rect.width // 2, 580)

def input_money():
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(150, 200, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text_color = pygame.Color('white')
    text = ''
    done = False
    prompt1 = "How much money do you want to"
    prompt2 = "deposit into the casino?"

    popup_width, popup_height = 500, 300
    popup_surface = pygame.Surface((popup_width, popup_height))
    popup_rect = popup_surface.get_rect(center=(new_width // 2, new_height // 2))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                translated_x = mouse_x - popup_rect.topleft[0]
                translated_y = mouse_y - popup_rect.topleft[1]

                if input_box.collidepoint((translated_x, translated_y)):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        with open("money.txt", "w") as file:
                            file.write(text)
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.blit(background, (0, 0))

        popup_surface.fill((0, 0, 0))

        prompt_surface1 = font.render(prompt1, True, pygame.Color('white'))
        prompt_surface2 = font.render(prompt2, True, pygame.Color('white'))
        popup_surface.blit(prompt_surface1, (20, 50))
        popup_surface.blit(prompt_surface2, (20, 100))

        txt_surface = font.render(text, True, text_color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        popup_surface.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(popup_surface, color, input_box, 2)

        screen.blit(popup_surface, popup_rect.topleft)

        pygame.display.flip()

def show_message(message):
    font = pygame.font.Font(None, 36)
    popup_width, popup_height = 500, 200
    popup_surface = pygame.Surface((popup_width, popup_height))
    popup_rect = popup_surface.get_rect(center=(new_width // 2, new_height // 2))

    message_done = False
    while not message_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                message_done = True

        screen.blit(background, (0, 0))

        popup_surface.fill((0, 0, 0))

        message_surface = font.render(message, True, pygame.Color('white'))
        popup_surface.blit(message_surface, (20, 50))

        screen.blit(popup_surface, popup_rect.topleft)

        pygame.display.flip()

def get_money():
    try:
        with open("money.txt", "r") as file:
            money = int(file.read().strip())
    except:
        money = 0
    return money

running = True
while running:
    money = get_money()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exchange_button_rect.collidepoint(event.pos):
                button_sound.play()
                input_money()
            elif play_button_rect.collidepoint(event.pos):
                button_sound.play()
                if money > 0:
                    running = False
                    pygame.quit()
                    subprocess.call([python_path, "black_jack.py"])
                else:
                    show_message("You didn't deposit the money")

    screen.blit(background, (0, 0))
    screen.blit(play_button_image, play_button_rect.topleft)
    screen.blit(exchange_button_image, exchange_button_rect.topleft)

    pygame.display.flip()

pygame.quit()
