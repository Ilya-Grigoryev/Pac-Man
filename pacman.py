import pygame


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
        self.rect = pygame.Rect(x*wall_size, y*wall_size, 4*wall_size, 4*wall_size)

    def draw(self):
        self.screen.blit(self.image, (self.rect.x-2*self.wall_size, self.rect.y-2*self.wall_size))

        if (self.rect.x - 2 * self.wall_size) <= 0:
            self.screen.blit(self.image,
                             (self.rect.x - 2 * self.wall_size + 56 * self.wall_size, self.rect.y - 2 * self.wall_size))
        if (self.rect.x + 2 * self.wall_size) >= 56 *  self.wall_size:
            self.screen.blit(self.image,
                             (self.rect.x - 2 * self.wall_size - 56 * self.wall_size, self.rect.y - 2 * self.wall_size))

        if (self.rect.x + 2 * self.wall_size) <= 0:
            self.rect.x += 56 * self.wall_size
            self.x = 54
        if (self.rect.x - 2 * self.wall_size) >= 56 *  self.wall_size:
            self.rect.x -= 56 * self.wall_size
            self.x = 1


    def update(self, walls, dots):
        self.change_dir()
        # if not self.is_collide(walls):
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
        try:
            x = self.x
            y = self.y
            return collide_dir == 'up' \
                and (self.level[y - 3][x] == '-'
                or self.level[y - 3][x-2] == '-'
                or self.level[y - 3][x+1] == '-') \
            or collide_dir == 'down' \
                and (self.level[y + 2][x] == '-'
                or self.level[y + 2][x-2] == '-'
                or self.level[y + 2][x+1] == '-') \
            or collide_dir == 'left' \
                and (self.level[y][x - 3] == '-'
                or self.level[y-2][x - 3] == '-'
                or self.level[y+1][x - 3] == '-') \
            or collide_dir == 'right'\
                and (self.level[y][x + 2] == '-'
                or self.level[y-2][x + 2] == '-'
                or self.level[y+1][x + 2] == '-')
        except IndexError as err:
            return collide_dir != 'right'
        # return self.rect.collidelist(list(map(lambda w: w.rect, walls))) != -1



    def change_dir(self):
        if not self.is_collide(self.newDir):
            self.dir = self.newDir