import random
import math
import pygame
import time


class Firework:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(2, 4)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(3, 7)
        self.lifetime = random.randint(20, 60)

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0


class FireworkAnimation:
    def __init__(self, screen, background_image_path, sound_file_path, screen_width=900, screen_height=515):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.fireworks = []
        self.running = True
        self.sound_on = True

        self.background = pygame.image.load(background_image_path)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        pygame.mixer.init()
        self.sound_file_path = sound_file_path
        pygame.mixer.music.load(self.sound_file_path)
        pygame.mixer.music.set_volume(0.1)

        self.font = pygame.font.Font(None, 200)

        self.sound_image = pygame.image.load('buttons/sound.png')
        self.sound_image = pygame.transform.scale(self.sound_image,
                                                  (int(0.15 * screen_width), int(0.15 * screen_height)))
        self.x_sound_image = pygame.image.load('buttons/x_sound.png')
        self.x_sound_image = pygame.transform.scale(self.x_sound_image,
                                                    (int(0.15 * screen_width), int(0.15 * screen_height)))

        self.sound_button_rect = self.sound_image.get_rect(bottomright=(self.screen_width, self.screen_height))

    def create_firework(self):
        x = random.randint(0, self.screen_width)
        y = random.randint(self.screen_height // 2, self.screen_height)
        color = random.choice(self.colors)
        for _ in range(random.randint(50, 100)):
            self.fireworks.append(Firework(x, y, color))

    def update_fireworks(self):
        self.fireworks = [f for f in self.fireworks if f.is_alive()]
        for f in self.fireworks:
            f.update()

    def draw_fireworks(self):
        self.screen.blit(self.background, (0, 0))
        for f in self.fireworks:
            pygame.draw.circle(self.screen, f.color, (int(f.x), int(f.y)), f.radius)
        text = self.font.render("You Win!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)

        if self.sound_on:
            self.screen.blit(self.sound_image, self.sound_button_rect)
        else:
            self.screen.blit(self.x_sound_image, self.sound_button_rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.sound_button_rect.collidepoint(event.pos):
                    self.toggle_sound()

    def toggle_sound(self):
        if self.sound_on:
            pygame.mixer.music.stop()
            self.sound_on = False
        else:
            pygame.mixer.music.play(-1)
            self.sound_on = True

    def run(self):
        clock = pygame.time.Clock()
        start_time = time.time()
        pygame.mixer.music.play(-1)

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > 4:
                self.running = False
                pygame.mixer.music.stop()

            self.handle_events()
            self.create_firework()
            self.update_fireworks()
            self.draw_fireworks()
            clock.tick(60)

        pygame.quit()


pygame.init()
screen = pygame.display.set_mode((900, 515))
pygame.display.set_caption("Fireworks Animation")

background_image_path = "rooms/table.PNG"
sound_file_path = "audio_files/fireworks.mp3"

fireworks_animation = FireworkAnimation(screen, background_image_path, sound_file_path)
fireworks_animation.run()