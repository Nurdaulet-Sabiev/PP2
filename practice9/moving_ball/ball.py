from __future__ import annotations

import pygame


class BallGame:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.radius = 25
        self.step = 20
        self.x = self.width // 2
        self.y = self.height // 2
        self.font = pygame.font.SysFont("arial", 24)

    def move(self, dx: int, dy: int) -> None:
        new_x = self.x + dx
        new_y = self.y + dy

        if new_x - self.radius < 0 or new_x + self.radius > self.width:
            new_x = self.x
        if new_y - self.radius < 0 or new_y + self.radius > self.height:
            new_y = self.y

        self.x = new_x
        self.y = new_y

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, (220, 30, 30), (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, (30, 30, 30), (self.x, self.y), self.radius, 2)

        info = self.font.render("Use arrow keys to move the ball by 20 pixels", True, (40, 40, 40))
        self.screen.blit(info, (20, 20))

        pos = self.font.render(f"Position: ({self.x}, {self.y})", True, (40, 40, 40))
        self.screen.blit(pos, (20, 55))

        pygame.display.flip()
