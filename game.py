import pygame
from block import Wall


class Game:
    def __init__(self, wall_size):
        self.wall_size = wall_size
        self.location = "menu"
        # сюда будем дописывать общие переменные

    def draw_level(self, screen):
        with open("level.txt", 'r') as f:
            level_arr = f.read().split('\n')
            screen.fill((0, 0, 0))
            for j, string in enumerate(level_arr):
                for i, char in enumerate(string):
                    if char == '-':
                        wall = Wall(i*self.wall_size, j*self.wall_size, self.wall_size)
                        wall.draw(screen)

    def update(self):
        pass