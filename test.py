import pygame
import subprocess
# Ścieżka do interpretera Pythona w środowisku wirtualnym
python_path = "C:/Users/patry/PycharmProjects/kasyno/c/Scripts/python.exe"

# Ścieżka do skryptu
script_path = "Black_Jack.py"
# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 768
PLAYER_SIZE_H = 160
PLAYER_SIZE_W = 60

# Define table interaction rectangles for each table
TABLE_INTERACTION_RECTS = [
    pygame.Rect(830, 580, 230, 130),
    pygame.Rect(485, 225, 160, 85),
    pygame.Rect(840, 225, 160, 85),
    pygame.Rect(965, 370, 200, 110),
    pygame.Rect(650, 370, 200, 110),
    pygame.Rect(310, 370, 200, 110),
    pygame.Rect(410, 580, 230, 130)
]

# Load button image
button_image = pygame.image.load('przycisk.png')  # Make sure the button image file exists

# Button class
class ImageButton:
    def __init__(self, center_pos, image, target_rect):
        self.original_image = image
        scale_width = target_rect.width / self.original_image.get_width()
        scale_height = target_rect.height / self.original_image.get_height()
        scale = min(scale_width, scale_height) * 1  # scale to fit within the rectangle, with some padding
        width = int(self.original_image.get_width() * scale)
        height = int(self.original_image.get_height() * scale)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect(center=center_pos)
        self.highlighted = False  # This now only controls visibility

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Player class with interaction capabilities
class Player:
    def __init__(self, images, position=(700, 600)):
        self.images = images
        self.position = list(position)
        self.direction = 'down'
        self.size = (PLAYER_SIZE_W, PLAYER_SIZE_H)

    def draw(self, screen):
        screen.blit(self.images[self.direction], self.position)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.position[0] -= 5
            self.direction = 'left'
        if keys[pygame.K_RIGHT]:
            self.position[0] += 5
            self.direction = 'right'
        if keys[pygame.K_UP]:
            self.position[1] -= 5
            self.direction = 'up'
        if keys[pygame.K_DOWN]:
            self.position[1] += 5
            self.direction = 'down'

    def check_interaction(self, interact_rects):
        player_rect = pygame.Rect(self.position[0], self.position[1], PLAYER_SIZE_W, PLAYER_SIZE_H)
        for interact_rect in interact_rects:
            if player_rect.colliderect(interact_rect):
                return interact_rect
        return None

def game_loop():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Casino Game Simulation')

    # Load and scale images
    background_image = pygame.image.load('rooms/blackjack.jpg')
    player_images = {
        'down': pygame.image.load('player/front.png'),
        'up': pygame.image.load('player/back.png'),
        'left': pygame.image.load('player/left.png'),
        'right': pygame.image.load('player/right.png')
    }

    # Scale player images
    for key in player_images:
        player_images[key] = pygame.transform.scale(player_images[key], (PLAYER_SIZE_W, PLAYER_SIZE_H))

    player = Player(player_images)
    buttons = [ImageButton(rect.center, button_image, rect) for rect in TABLE_INTERACTION_RECTS]

    # Setup clock
    clock = pygame.time.Clock()
    running = True
    interact_rect = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and interact_rect:
                    for button in buttons:
                        if button.rect.colliderect(interact_rect):
                            subprocess.call([python_path, script_path])

        keys = pygame.key.get_pressed()
        player.move(keys)

        interact_rect = player.check_interaction(TABLE_INTERACTION_RECTS)

        screen.blit(background_image, (0, 0))
        player.draw(screen)

        # Update button visibility state based on proximity
        for button in buttons:
            button.highlighted = button.rect.colliderect(interact_rect) if interact_rect else False
            if button.highlighted:
                button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Start the game loop
game_loop()
