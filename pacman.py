import pygame

#from records import Records

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
        self.rect = pygame.Rect(x*wall_size-2*self.wall_size, y*wall_size-2*self.wall_size, 4*wall_size, 4*wall_size)
        self.food_counter = 0
        #self.record = Records

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        if self.rect.x <= 0:
            self.screen.blit(self.image,
                             (self.rect.x + 56 * self.wall_size, self.rect.y))
        if (self.rect.x + 4 * self.wall_size) >= 56 * self.wall_size:
            self.screen.blit(self.image,
                             (self.rect.x - 56 * self.wall_size, self.rect.y))

        if (self.rect.x + 4 * self.wall_size) <= 0:
            self.rect.x += 56 * self.wall_size
            self.x = 52
        if self.rect.x >= 56 * self.wall_size:
            self.rect.x -= 56 * self.wall_size
            self.x = 0


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

        for dot in dots:
            if dot.rect.colliderect(self.rect):
                dots.pop(dots.index(dot))
                self.food_counter += 1
               # self.record.add(self.food_counter)
                print(self.food_counter)

        self.draw()

    def is_collide(self, collide_dir):
        try:
            x = self.x
            y = self.y
            return collide_dir == 'up' \
                and (self.level[y - 1][x] == '-'
                or self.level[y - 1][x+1] == '-'
                or self.level[y - 1][x+3] == '-') \
            or collide_dir == 'down' \
                and (self.level[y+4][x] == '-'
                or self.level[y+4][x+1] == '-'
                or self.level[y+4][x+3] == '-') \
            or collide_dir == 'left' \
                and (self.level[y][x - 1] == '-'
                or self.level[y+1][x - 1] == '-'
                or self.level[y+3][x - 1] == '-') \
            or collide_dir == 'right' \
                and (self.level[y][x+4] == '-'
                or self.level[y+1][x+4] == '-'
                or self.level[y+3][x+4] == '-')
        except IndexError as err:
            return collide_dir != 'right'
        # return self.rect.collidelist(list(map(lambda w: w.rect, walls))) != -1



    def change_dir(self):
        if not self.is_collide(self.newDir):
            self.dir = self.newDir