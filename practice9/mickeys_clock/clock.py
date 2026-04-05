from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pygame


@dataclass
class ClockColors:
    background: tuple[int, int, int] = (245, 240, 230)
    face: tuple[int, int, int] = (255, 255, 255)
    outline: tuple[int, int, int] = (40, 40, 40)
    tick: tuple[int, int, int] = (70, 70, 70)
    accent: tuple[int, int, int] = (180, 40, 40)


class MickeyClock:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.center = (self.w // 2, self.h // 2 + 30)
        self.colors = ClockColors()
        self.font_big = pygame.font.SysFont("arial", 54, bold=True)
        self.font_small = pygame.font.SysFont("arial", 22)

        image_path = Path(__file__).parent / "images" / "mickey_hand.png"
        self.hand_image = pygame.image.load(str(image_path)).convert_alpha()
        self.hand_rect = self.hand_image.get_rect()

    @staticmethod
    def _rotate_image(image: pygame.Surface, angle: float) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotozoom(image, angle, 1.0)
        rect = rotated.get_rect()
        return rotated, rect

    def _draw_face(self) -> None:
        pygame.draw.circle(self.screen, self.colors.outline, self.center, 182)
        pygame.draw.circle(self.screen, self.colors.face, self.center, 172)

        # simple minute markers
        for i in range(60):
            angle = -i * 6
            length = 12 if i % 5 == 0 else 6
            width = 4 if i % 5 == 0 else 2
            marker = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.rect(marker, self.colors.tick, (4, 0, width, length))
            rotated, rect = self._rotate_image(marker, angle)
            rect.center = self.center
            rect.move_ip(0, -150)
            self.screen.blit(rotated, rect)

        # inner center dot
        pygame.draw.circle(self.screen, self.colors.outline, self.center, 10)
        pygame.draw.circle(self.screen, self.colors.accent, self.center, 5)

    def _blit_hand(self, angle: float, scale: float, offset_y: int = 0) -> None:
        image = pygame.transform.smoothscale(
            self.hand_image,
            (int(self.hand_rect.width * scale), int(self.hand_rect.height * scale)),
        )
        rotated, rect = self._rotate_image(image, angle)
        rect.center = self.center
        rect.y += offset_y
        self.screen.blit(rotated, rect)

    def draw(self) -> None:
        now = datetime.now()
        minute = now.minute
        second = now.second

        self.screen.fill(self.colors.background)
        self._draw_face()

        # Hands are aligned to 0 degrees pointing up in the asset.
        second_angle = -second * 6
        minute_angle = -minute * 6

        # left hand = seconds, right hand = minutes
        self._blit_hand(minute_angle, scale=0.82)
        self._blit_hand(second_angle, scale=0.72, offset_y=6)

        time_text = f"{minute:02d}:{second:02d}"
        text = self.font_big.render(time_text, True, self.colors.outline)
        text_rect = text.get_rect(center=(self.w // 2, 95))
        self.screen.blit(text, text_rect)

        caption = self.font_small.render("Minutes on the right hand, seconds on the left hand", True, self.colors.outline)
        caption_rect = caption.get_rect(center=(self.w // 2, self.h - 35))
        self.screen.blit(caption, caption_rect)

        pygame.display.flip()
