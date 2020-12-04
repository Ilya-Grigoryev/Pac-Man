import pygame
import sys

from game import Game


def draw_menu(window, font, game):
    window.fill((0, 0, 0))
    text = font.render("PAC-MAN", True, (225, 255, 77))
    window_rect = window.get_rect()
    window.blit(text, text.get_rect(center=(window_rect.centerx, window_rect.centery - 300)))

    text = font.render("Records (TOP 5):", True, (139, 153, 168))
    window.blit(text, text.get_rect(center=(window_rect.centerx, window_rect.centery - 200)))

    for i in range(len(game.scores)):
        if i == 5:
            break
        text = font.render(f"{i+1}.  {game.scores[i]}", True, (139, 153, 168))
        window.blit(text, (window_rect.centerx-90, window_rect.centery - 150 + i*40))
        pygame.draw.rect(window, (139, 153, 168),
                         (window_rect.centerx - 100, window_rect.centery - 154 + i*40, 200, 40), 2)
    text = font.render("Press space to continue", True, (139, 153, 168))
    window.blit(text, text.get_rect(center=(window_rect.centerx, window_rect.centery + 300)))


WALL_SIZE = 20


def main():
    pygame.init()
    pygame.display.set_caption("Pac-Man")
    window = pygame.display.set_mode((WALL_SIZE * 28, WALL_SIZE * 31 + 150))
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("textures/fonts/font.otf", 50)

    game = Game(WALL_SIZE)

    while not game.game_over:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game.location == 'menu':
                    if event.key == pygame.K_SPACE:
                        game.location = "level " + str(game.level)
                        game.start(window, is_restart=True)
                        pygame.display.update()
                elif game.location == 'level ' + str(game.level):
                    if event.key == pygame.K_w or event.key == 1094:
                        game.pacman.newDir = 'up'
                    elif event.key == pygame.K_a or event.key == 1092:
                        game.pacman.newDir = 'left'
                    elif event.key == pygame.K_s or event.key == 1099:
                        game.pacman.newDir = 'down'
                    elif event.key == pygame.K_d or event.key == 1074:
                        game.pacman.newDir = 'right'

        if game.location == "menu":
            draw_menu(window, title_font, game)
        else:
            game.update(window)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
