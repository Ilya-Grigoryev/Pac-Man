import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)