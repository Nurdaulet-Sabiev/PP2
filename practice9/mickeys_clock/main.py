from __future__ import annotations

import sys

import pygame

from clock import MickeyClock


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Mickey's Clock")
    screen = pygame.display.set_mode((700, 700))
    clock = pygame.time.Clock()
    app = MickeyClock(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

        app.draw()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
