import pygame


class Bigdot(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.rect.centerx, self.rect.centery), self.size)