import pygame
import time

from block import Wall
from dot import Dot
from pacman import Pacman
from ghosts import Speedy
from bigdots import Bigdot


# from records import Records


class Game:
    def __init__(self, wall_size):
        self.time = time.time()
        self.is_runaway = False
        self.runaway_time = 6
        self.wall_size = wall_size
        self.location = "menu"
        self.map = None
        self.pacman = None
        self.ghosts = []
        self.walls = []
        self.dots = []
        self.bigdots = []
        self.level_over = False
        self.game_over = False
        self.level = 1
        self.font = pygame.font.Font('textures/fonts/arcade_classic.ttf', 36)
        self.score = 0
        self.health = 2
        self.bg_surf = pygame.image.load('textures/map.png')
        self.bg_surf = pygame.transform.scale(self.bg_surf, (28*self.wall_size, 31*self.wall_size))
        self.bg_rect = self.bg_surf.get_rect()
        self.bg_rect = self.bg_rect.move(0, 100)
        self.scores = self.read_scores()
        # сюда будем дописывать общие переменные

    def read_scores(self):
        try:
            with open('records.txt', 'r') as f:
                arr = []
                for score in f.read().split('\n'):
                    try:
                        arr.append(int(score))
                    except ValueError:
                        continue
                return arr
        except FileNotFoundError:
            with open('records.txt', 'w'):
                return []

    def save_scores(self, scores):
        with open('records.txt', 'w') as f:
            scores.sort(reverse=True)
            scores = list(map(str, scores))
            f.write('\n'.join(scores))

    def start(self, screen, is_restart=False, is_new_level=False):
        if is_restart:
            self.health = 2
            self.score = 0
            self.level = 1
        with open("level.txt", 'r') as f:
            self.map = f.read().split('\n')
        if is_restart:
            self.pacman = Pacman(screen, 13.5, 23, self.map, self.wall_size)
        else:
            last_pacman_score = self.pacman.score
            self.pacman = Pacman(screen, 13.5, 23, self.map, self.wall_size)
            self.pacman.score = last_pacman_score
        self.ghosts = []
        if is_restart:
            self.bigdots = []
            self.dots = []
        self.ghosts.append(Speedy(screen, 12, 13, 'red', self.map, self.wall_size, self.pacman))
        self.ghosts.append(Speedy(screen, 15, 13, 'yellow', self.map, self.wall_size, self.pacman))
        self.ghosts.append(Speedy(screen, 12, 15, 'blue', self.map, self.wall_size, self.pacman))
        self.ghosts.append(Speedy(screen, 15, 15, 'pink', self.map, self.wall_size, self.pacman))

        for j, string in enumerate(self.map):
            for i, char in enumerate(string):
                if char == '-':
                    wall = Wall(i * self.wall_size, j * self.wall_size + 100, self.wall_size)
                    self.walls.append(wall)
                elif char == '*' and (is_restart or is_new_level):
                    food = Dot(i * self.wall_size + self.wall_size // 2,
                               j * self.wall_size + 100 + self.wall_size // 2, self.wall_size // 6)
                    self.dots.append(food)
                elif char == '+' and (is_restart or is_new_level):
                    bigfood = Bigdot(i * self.wall_size + self.wall_size // 2,
                                     j * self.wall_size + 100 + self.wall_size // 2, self.wall_size // 2.5)
                    self.bigdots.append(bigfood)

    def update(self, screen):
        #  отрисовка
        screen.fill((0, 0, 0))
        screen.blit(self.bg_surf, self.bg_rect)
        # for wall in self.walls:
        #     wall.draw(screen)
        for dot in self.dots:
            dot.draw(screen)
        for bigdot in self.bigdots:
            bigdot.draw(screen)

        #  проверка на режим разбегания
        if self.is_runaway and time.time() - self.time >= self.runaway_time:
            self.off_runway()

        # обновление Pac-Man
        self.pacman.update(self.walls, self.dots)

        # обновление привидений
        for ghost in self.ghosts:
            ghost.update()

        #  проверка на съедание большой точки
        for bigot in self.bigdots:
            if bigot.rect.colliderect(self.pacman.rect):
                self.bigdots.pop(self.bigdots.index(bigot))
                self.pacman.score += 30
                self.on_runaway()

        # проверка на съедение всех точек
        if len(self.dots) == 0 and len(self.bigdots) == 0:
            self.score += self.pacman.score
            self.level += 1
            self.location = "level"
            self.level_over = False
            self.start(screen, is_new_level=True)

        #  проверка на столкновение с привидением
        for ghost in self.ghosts:
            if self.pacman.rect.colliderect(ghost.rect):
                if not ghost.runaway:
                    self.health -= 1
                    if self.health == 0:
                        self.location = "menu"
                        self.scores.append(self.score + self.pacman.score)
                        self.save_scores(self.scores)
                    else:
                        self.start(screen)

                elif ghost.state == "lives":
                    self.pacman.kills += 1
                    self.pacman.score += self.pacman.kills * 200
                    ghost.kill()
                break

        # обновление TopBar
        self.update_TopBar(screen)

        # обновление BottomBar
        self.update_BottomBar(screen)

    def on_runaway(self):
        for ghost in self.ghosts:
            ghost.runaway_start()

    def off_runway(self):
        for ghost in self.ghosts:
            ghost.runaway_finish()

    def update_TopBar(self, screen):
        score_text = self.font.render(f'Score {self.score + self.pacman.score}', True, (220, 220, 220))
        level_text = self.font.render(f'Level {self.level}', True, (220, 220, 220))
        screen.blit(score_text, (10, 50))
        screen.blit(level_text, (10, 10))

    def update_BottomBar(self, screen):
        health_text = self.font.render(f'Health {self.health}', True, (220, 220, 220))
        screen.blit(health_text, (10, 100 + self.wall_size*31 + 20))