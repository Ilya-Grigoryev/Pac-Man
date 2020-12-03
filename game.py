import pygame

from block import Wall
from dot import Dot
from pacman import Pacman
from ghosts import Speedy
from bigdots import Bigdot


# from records import Records


class Game:
    def __init__(self, wall_size):
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
        # сюда будем дописывать общие переменные

    def start(self, screen, is_restart=False):
        if is_restart:
            self.health = 2
        with open("level.txt", 'r') as f:
            self.map = f.read().split('\n')

        self.pacman = Pacman(screen, 13.5, 23, self.map, self.wall_size)
        self.ghosts = []
        self.ghosts.append(Speedy(screen, 11, 13, 'red', self.map, self.wall_size))
        self.ghosts.append(Speedy(screen, 14, 13, 'red', self.map, self.wall_size))

        for j, string in enumerate(self.map):
            for i, char in enumerate(string):
                if char == '-':
                    wall = Wall(i * self.wall_size, j * self.wall_size + 100, self.wall_size)
                    self.walls.append(wall)
                elif char == '*':
                    food = Dot(i * self.wall_size + self.wall_size // 2,
                               j * self.wall_size + 100 + self.wall_size // 2, self.wall_size // 6)
                    self.dots.append(food)
                elif char == '+':
                    bigfood = Bigdot(i * self.wall_size + self.wall_size // 2,
                                     j * self.wall_size + 100 + self.wall_size // 2, self.wall_size // 2.5)
                    self.bigdots.append(bigfood)

    def update(self, screen):
        screen.fill((0, 0, 0))

        for wall in self.walls:
            wall.draw(screen)
        for dot in self.dots:
            dot.draw(screen)
        for bigdot in self.bigdots:
            bigdot.draw(screen)

        # обновление Pac-Man
        self.pacman.update(self.walls, self.dots, self.bigdots)
        for ghost in self.ghosts:
            ghost.update()

        # проверка на съедение всех точек
        if len(self.dots) == 0 and len(self.bigdots) == 0:
            self.score += self.pacman.score
            self.level += 1
            self.location = "level " + str(self.level)
            self.level_over = False
            self.start(screen)

        #  проверка на столкновение с привидением
        for ghost in self.ghosts:
            if self.pacman.rect.colliderect(ghost.rect):
                self.start(screen)
                self.health -= 1
                if self.health == 0:
                    self.location = "menu"


        # обновление TopBar
        self.update_TopBar(screen)

        # обновление BottomBar
        self.update_BottomBar(screen)

    def update_TopBar(self, screen):
        score_text = self.font.render(f'Score {self.score + self.pacman.score}', True, (220, 220, 220))
        level_text = self.font.render(f'Level {self.level}', True, (220, 220, 220))
        screen.blit(score_text, (10, 50))
        screen.blit(level_text, (10, 10))

    def update_BottomBar(self, screen):
        health_text = self.font.render(f'Health {self.health}', True, (220, 220, 220))
        screen.blit(health_text, (10, 100 + self.wall_size*31 + 20))