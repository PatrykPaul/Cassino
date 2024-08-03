import pygame
import sys


class Exit_Button:
    def __init__(self, screen, image_path, position):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        original_size = self.image.get_size()
        new_size = (int(original_size[0] * 0.12), int(original_size[1] * 0.12))
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()
        self.rect.topright = position

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
