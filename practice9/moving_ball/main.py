from __future__ import annotations

import sys

import pygame

from ball import BallGame


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Moving Ball Game")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    game = BallGame(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_LEFT:
                    game.move(-game.step, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(game.step, 0)
                elif event.key == pygame.K_UP:
                    game.move(0, -game.step)
                elif event.key == pygame.K_DOWN:
                    game.move(0, game.step)

        game.draw()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
