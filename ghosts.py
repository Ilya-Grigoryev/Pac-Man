import pygame
import random
import time


class Speedy:
    def __init__(self, screen, x, y, color, level, wall_size):
        self.screen = screen
        self.speed = 0.5
        self.x, self.y = float(x), float(y)
        self.color = color
        self.level = level
        self.wall_size = wall_size
        self.image = pygame.Surface((self.wall_size, self.wall_size))
        self.image.fill(pygame.Color(220, 0, 0))
        self.rect = pygame.Rect(x * wall_size, y * wall_size + 100, wall_size, wall_size)
        self.route = []
        self.targets = []
        for maze_y, string in enumerate(self.level):
            for maze_x, char in enumerate(string):
                if char != '-' and char != '.':
                    self.targets.append((maze_y, maze_x))
        self.delta_time = 5
        self.time = time.time() - self.delta_time
        self.create_route()

    def update(self):
        self.create_route()
        # print(f"len(route) = {len(self.route)}")
        self.rect.x = (self.x * self.wall_size)
        self.rect.y = (self.y * self.wall_size + 100)
        self.draw()
        self.y, self.x = self.route.pop(0)

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def create_route(self):
        if not ((self.x % 1 == 0 and self.y % 1 == 0) and (time.time() - self.time >= self.delta_time)):
            if len(self.route) > 1:
                return None
        bfs_route = self.__bfs()
        while not bfs_route:
            bfs_route = self.__bfs()
        self.route = []
        for i, (cage_y, cage_x) in enumerate(bfs_route[:-1]):
            if cage_y != bfs_route[i + 1][0]:
                delta = 1 * self.speed if cage_y < bfs_route[i + 1][0] else -1 * self.speed
                y = cage_y
                while y < bfs_route[i + 1][0]:
                    self.route.append((y, cage_x))
                    y += delta
                y = cage_y
                while y > bfs_route[i + 1][0]:
                    self.route.append((y, cage_x))
                    y += delta
            elif cage_x != bfs_route[i + 1][1]:
                delta = 1 * self.speed if cage_x < bfs_route[i + 1][1] else -1 * self.speed
                x = cage_x
                # print(f"{x} < {bfs_route[i + 1][1]}, delta: {delta}")
                while x < bfs_route[i + 1][1]:
                    self.route.append((cage_y, x))
                    x += delta
                x = cage_x
                while x > bfs_route[i + 1][1]:
                    self.route.append((cage_y, x))
                    x += delta
        # self.route.append(bfs_route[-1])
        # print("route:", self.route)
        self.time = time.time()

    def __bfs(self):
        maze = []
        for string in self.level:
            maze.append(string)
        maze[int(self.y)] = maze[int(self.y)][:int(self.x)] + 'S' + maze[int(self.y)][int(self.x)+1:]
        target_y, target_x = self.__choose_target()
        while int(self.y) == target_y and int(self.x) == target_x:
            target_y, target_x = self.__choose_target()
        maze[target_y] = maze[target_y][:target_x] + 'F' + maze[target_y][target_x+1:]
        r = next(i for i, line in enumerate(maze) if "S" in line)
        c = maze[r].index("S")
        queue = []
        visited = {(r, c): (-1, -1)}
        queue.append((r, c))
        while len(queue) > 0:
            r, c = queue.pop(0)
            if maze[r][c] == 'F':
                path = []
                while r != -1:
                    path.append((r, c))
                    r, c = visited[(r, c)]
                path.reverse()
                # path.pop(0)
                # print(path)
                return path
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                new_r = r + dy
                new_c = c + dx
                if (0 <= new_r < len(maze) and
                        0 <= new_c < len(maze[0]) and
                        not (new_r, new_c) in visited and
                        maze[new_r][new_c] != '-'):
                    visited[(new_r, new_c)] = (r, c)
                    queue.append((new_r, new_c))

    def __choose_target(self):
        return random.choice(self.targets)
