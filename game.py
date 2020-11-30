import pygame

from block import Wall
from dot import Dot
from pacman import Pacman
from bigdots import Bigdot
#from records import Records


class Game:
    def __init__(self, wall_size):
        self.wall_size = wall_size
        self.location = "menu"
        self.map = None
        self.pacman = None
        self.level_over = False
        self.level = 1
        self.font = pygame.font.Font('textures/fonts/arcade_classic.ttf', 36)
        self.score = 0
        # сюда будем дописывать общие переменные

    def start(self, screen):
        with open("level.txt", 'r') as f:
            self.map = f.read().split('\n')

        self.pacman = Pacman(screen, 26, 46, self.map, self.wall_size)

        self.walls = []
        self.dots = []
        self.bigdots = []

        for j, string in enumerate(self.map):
            for i, char in enumerate(string):
                if char == '-':
                    wall = Wall(i * self.wall_size, j * self.wall_size+100, self.wall_size)
                    self.walls.append(wall)
                elif char == '*':
                    food = Dot(i * self.wall_size, j * self.wall_size+100, self.wall_size//2)
                    self.dots.append(food)
                elif char == '+':
                    bigfood = Bigdot(i * self.wall_size, j * self.wall_size+100, self.wall_size)
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
        # self.pacman.update(self.walls, self.dots)
        self.pacman.update(self.walls, self.dots, self.bigdots)

        # проверка на съедение всех точек
        if len(self.dots) == 0:
            self.score += self.pacman.score
            self.level += 1
            self.location = "level " + str(self.level)
            self.level_over = False
            self.start(screen)

        # обновление TopBar
        self.update_TopBar(screen)


    def update_TopBar(self, screen):
        score_text = self.font.render(f'Score {self.score+self.pacman.score}', True, (220, 220, 220))
        level_text = self.font.render(f'Level {self.level}', True, (220, 220, 220))
        screen.blit(score_text, (10, 50))
        screen.blit(level_text, (10, 10))
