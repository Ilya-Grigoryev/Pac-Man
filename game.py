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
        self.level = None
        self.pacman = None
        # сюда будем дописывать общие переменные

    def start(self, screen):
        with open("level.txt", 'r') as f:
            self.level = f.read().split('\n')

        self.pacman = Pacman(screen, 28, 47, self.level, self.wall_size)

        self.walls = []
        self.dots = []
        self.bigdots = []

        for j, string in enumerate(self.level):
            for i, char in enumerate(string):
                if char == '-':
                    wall = Wall(i * self.wall_size, j * self.wall_size, self.wall_size)
                    self.walls.append(wall)
                elif char == '*':
                    food = Dot(i * self.wall_size, j * self.wall_size, self.wall_size//2)
                    self.dots.append(food)
                elif char == '+':
                    bigfood = Bigdot(i * self.wall_size, j * self.wall_size, self.wall_size)
                    self.bigdots.append(bigfood)

    def update(self, screen):
        screen.fill((0, 0, 0))

        for wall in self.walls:
            wall.draw(screen)
        for dot in self.dots:
            dot.draw(screen)
        for bigdot in self.bigdots:
            bigdot.draw(screen)

        self.pacman.update(self.walls, self.dots, self.bigdots)