import pygame


class Pacman(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, level, wall_size):
        super().__init__()
        self.screen = screen
        self.level = level
        self.wall_size = wall_size
        self.x, self.y = float(x), float(y)
        self.speed = 0.5
        self.dir = 'up'
        self.newDir = 'up'
        # self.image = pygame.Surface((self.wall_size, self.wall_size))
        # self.image.fill(pygame.Color(255, 255, 0))
        self.rect = pygame.Rect(x*wall_size, y*wall_size+100, wall_size, wall_size)
        self.img_surf = {
            'down': [pygame.image.load(f'textures/pacman/down/{i}.png') for i in range(1, 3 + 1)],
            'left': [pygame.image.load(f'textures/pacman/left/{i}.png') for i in range(1, 3 + 1)],
            'right': [pygame.image.load(f'textures/pacman/right/{i}.png') for i in range(1, 3 + 1)],
            'up': [pygame.image.load(f'textures/pacman/up/{i}.png') for i in range(1, 3 + 1)]
        }
        self.img_index = 2
        self.img_index_dir = 1
        self.score = 0
        self.kills = 0

    def draw(self):
        if self.img_index == 3 or self.img_index == 1:
            self.img_index_dir *= -1
        self.img_index += self.img_index_dir
        if self.is_collide(self.dir):
            self.img_index = 2
        self.screen.blit(self.img_surf[self.dir][self.img_index-1], (self.rect.x, self.rect.y))

        if self.rect.x <= 0:
            self.screen.blit(self.img_surf[self.dir][self.img_index - 1],
                             (self.rect.x + 28 * self.wall_size, self.rect.y))
        if (self.rect.x + self.wall_size) >= 28 * self.wall_size:
            self.screen.blit(self.img_surf[self.dir][self.img_index - 1],
                             (self.rect.x - 28 * self.wall_size, self.rect.y))

        if (self.rect.x + self.wall_size) <= 0:
            self.rect.x += 28 * self.wall_size
            self.x = 27
        if self.rect.x >= 28 * self.wall_size:
            self.rect.x -= 28 * self.wall_size
            self.x = 0

    def update(self, walls, dots):
        self.change_dir()
        if not self.is_collide(self.dir):
            if self.dir == 'up':
                self.y -= self.speed
            elif self.dir == 'down':
                self.y += self.speed
            elif self.dir == 'left':
                self.x -= self.speed
            elif self.dir == 'right':
                self.x += self.speed
            self.rect.x = (self.x * self.wall_size)
            self.rect.y = (self.y * self.wall_size + 100)

        for dot in dots:
            if dot.rect.colliderect(self.rect):
                dots.pop(dots.index(dot))
                self.score += 10

        self.draw()

    def is_collide(self, collide_dir):
        try:
            if (collide_dir == 'up' or collide_dir == 'down') and (self.y % 1 != 0) \
                    or (collide_dir == 'left' or collide_dir == 'right') and (self.x % 1 != 0):
                return False

            x = int(self.x)
            y = int(self.y)

            return collide_dir == 'up' and self.level[y-1][x] == '-' \
                   or collide_dir == 'down' and self.level[y+1][x] == '-' \
                   or collide_dir == 'left' and self.level[y][x-1] == '-' \
                   or collide_dir == 'right' and self.level[y][x+1] == '-'
        except IndexError:
            return collide_dir != 'right'

    def change_dir(self):
        if (self.newDir == 'up' or self.newDir == 'down') and self.x % 1 != 0 \
        or (self.newDir == 'left' or self.newDir == 'right') and self.y % 1 != 0:
            return
        if not self.is_collide(self.newDir):
            self.dir = self.newDir