import pygame

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 768
PLAYER_SIZE_H = 160
PLAYER_SIZE_W = 60
FONT_COLOR = (255, 215, 0)  # Gold color for the text
BUTTON_COLOR = (200, 0, 0)  # Red color for the button background
BUTTON_PULSE_COLOR = (255, 20, 20)  # Slightly lighter red for animation

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


font = pygame.font.SysFont('timesnewroman', 26)

# Player class with interaction capabilities
class Player:
    def __init__(self, images, position=(700, 600)):
        self.images = images
        self.position = list(position)
        self.direction = 'down'
        self.size = (PLAYER_SIZE_W, PLAYER_SIZE_H)
        self.interact = False

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
    # Initialize graphics
    background_image = pygame.image.load('rooms/blackjack.jpg')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Casino Game Simulation')

    # Create player
    player_images = {
        'down': pygame.image.load('player/front.png'),
        'up': pygame.image.load('player/back.png'),
        'left': pygame.image.load('player/left.png'),
        'right': pygame.image.load('player/right.png')
    }

    # Scale images
    for key in player_images:
        player_images[key] = pygame.transform.scale(player_images[key], (PLAYER_SIZE_W, PLAYER_SIZE_H))

    player = Player(player_images)

    # Setup clock
    clock = pygame.time.Clock()
    running = True
    button_rect = None  # Initialize button rectangle for drawing
    button_animation_counter = 0  # Counter for button animation

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and interact_rect:
                    print("Graj")

        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Check for interaction with the tables
        interact_rect = player.check_interaction(TABLE_INTERACTION_RECTS)

        # Draw everything
        screen.blit(background_image, (0, 0))
        player.draw(screen)

        # If player can interact with a table, show the play button
        if interact_rect:
            button_text = font.render("Graj", True, FONT_COLOR)
            button_rect = button_text.get_rect(center=interact_rect.center)
            button_color = BUTTON_COLOR if button_animation_counter % 60 < 30 else BUTTON_PULSE_COLOR
            pygame.draw.rect(screen, button_color, button_rect.inflate(20, 10))
            screen.blit(button_text, button_rect)

        button_animation_counter += 1  # Increase animation counter
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Start the game loop
game_loop()
