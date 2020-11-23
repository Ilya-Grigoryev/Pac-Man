import pygame
import time


class Pacman(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, level, wall_size):
        super().__init__()
        self.screen = screen
        self.level = level
        self.wall_size = wall_size
        self.x, self.y = x, y
        self.speed = 1
        self.dir = 'up'
        self.newDir = 'up'
        self.image = pygame.Surface((self.wall_size*4, self.wall_size*4))
        self.image.fill(pygame.Color(255, 255, 0))
        self.rect = pygame.Rect((x)*wall_size, (y)*wall_size, 4*wall_size, 4*wall_size)
        self.time = time.time()

    def draw(self):
        self.screen.blit(self.image, (self.rect.x-2*self.wall_size, self.rect.y-2*self.wall_size))

    def update(self):
        # if time.time() - self.time < 100:
        #     return
        self.time = time.time()
        self.change_dir()
        # self.x % 1.0 == 0 or self.y % 1.0 == 0 and
        if not self.is_collide(self.dir):
            if self.dir == 'up':
                self.y -= self.speed
            elif self.dir  == 'down':
                self.y += self.speed
            elif self.dir == 'left':
                self.x -= self.speed
            elif self.dir == 'right':
                self.x += self.speed
            self.rect.x = (self.x * self.wall_size)
            self.rect.y = (self.y * self.wall_size)
        self.draw()

    def is_collide(self, collide_dir):
        return collide_dir == 'up' \
            and (self.level[self.y - 3][self.x] == '-'
            or self.level[self.y - 3][self.x-2] == '-'
            or self.level[self.y - 3][self.x+1] == '-') \
        or collide_dir == 'down' \
            and (self.level[self.y + 2][self.x] == '-'
            or self.level[self.y + 2][self.x-2] == '-'
            or self.level[self.y + 2][self.x+1] == '-') \
        or collide_dir == 'left' \
            and (self.level[self.y][self.x - 3] == '-'
            or self.level[self.y-2][self.x - 3] == '-'
            or self.level[self.y+1][self.x - 3] == '-') \
        or collide_dir == 'right'\
            and (self.level[self.y][self.x + 2] == '-'
            or self.level[self.y-2][self.x + 2] == '-'
            or self.level[self.y+1][self.x + 2] == '-')


    def change_dir(self):
        if not self.is_collide(self.newDir):
            self.dir = self.newDir