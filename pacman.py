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
        self.image = pygame.Surface((self.wall_size, self.wall_size))
        self.image.fill(pygame.Color(255, 255, 0))
        self.rect = pygame.Rect(x*wall_size, y*wall_size+100, wall_size, wall_size)
        self.score = 0

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        if self.rect.x <= 0:
            self.screen.blit(self.image,
                             (self.rect.x + 28 * self.wall_size, self.rect.y))
        if (self.rect.x + self.wall_size) >= 28 * self.wall_size:
            self.screen.blit(self.image,
                             (self.rect.x - 28 * self.wall_size, self.rect.y))

        if (self.rect.x + self.wall_size) <= 0:
            self.rect.x += 28 * self.wall_size
            self.x = 27
        if self.rect.x >= 28 * self.wall_size:
            self.rect.x -= 28 * self.wall_size
            self.x = 0


    def update(self, walls, dots, bigdots):
        self.change_dir()
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
            self.rect.y = (self.y * self.wall_size + 100)


        for dot in dots:
            if dot.rect.colliderect(self.rect):
                dots.pop(dots.index(dot))
                self.score += 10

        for bigot in bigdots:
            if bigot.rect.colliderect(self.rect):
                bigdots.pop(bigdots.index(bigot))
                self.score += 30

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