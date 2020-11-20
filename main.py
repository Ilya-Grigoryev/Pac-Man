import pygame
import sys

from game  import Game


def draw_menu(window, font):
    window.fill((0, 0, 0))
    text = font.render("PAC-MAN", True, (225, 255, 77))
    window_rect = window.get_rect()
    window.blit(text, text.get_rect(center=(window_rect.centerx, window_rect.centery-200)))
    pygame.draw.rect(window, (0, 0, 0), (window_rect.centerx-100, window_rect.centery-25, 200, 50))
    text = font.render("Press space to continue", True, (139, 153, 168))
    window.blit(text, text.get_rect(center=window_rect.center))


WALL_SIZE = 10


def main():
    pygame.init()
    pygame.display.set_caption("Pac-Man")
    window = pygame.display.set_mode((WALL_SIZE * 56, WALL_SIZE * 62))

    title_font = pygame.font.SysFont("textures/fonts/font.otf", 50)

    game = Game(WALL_SIZE)

    game_over = False
    while not game_over:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.location = "level 1"
                    game.draw_level(window)
                    pygame.display.update()

        if game.location == "menu":
            draw_menu(window, title_font)
        else:
            game.update()


        pygame.display.update()
        pygame.time.delay(10)


if __name__ == '__main__':
    main()