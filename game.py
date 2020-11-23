import pygame
from block import Wall
from pacman import Pacman


class Game:
    def __init__(self, wall_size):
        self.wall_size = wall_size
        self.location = "menu"
        self.level = None
        self.pacman = None
        # self.entities = pygame.sprite.Group()
        # сюда будем дописывать общие переменные

    def start(self, screen):
        # draw level
        with open("level.txt", 'r') as f:
            self.level = f.read().split('\n')

        # draw pac-man
        self.pacman = Pacman(screen, 28, 47, self.level, self.wall_size)
        # self.pacman.draw()


    def update(self, screen):
        screen.fill((0, 0, 0))
        for j, string in enumerate(self.level):
            for i, char in enumerate(string):
                if char == '-':
                    wall = Wall(i * self.wall_size, j * self.wall_size, self.wall_size)
                    wall.draw(screen)

        self.pacman.update()