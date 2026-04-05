from __future__ import annotations

import sys
from pathlib import Path

import pygame

from player import MusicPlayer


def fmt_time(seconds: float) -> str:
    total = max(0, int(seconds))
    m, s = divmod(total, 60)
    return f"{m:02d}:{s:02d}"


def draw_progress_bar(screen: pygame.Surface, x: int, y: int, w: int, h: int, ratio: float) -> None:
    pygame.draw.rect(screen, (60, 60, 60), (x, y, w, h), border_radius=8)
    fill_w = max(0, min(w, int(w * ratio)))
    if fill_w > 0:
        pygame.draw.rect(screen, (30, 150, 70), (x, y, fill_w, h), border_radius=8)
    pygame.draw.rect(screen, (20, 20, 20), (x, y, w, h), 2, border_radius=8)


def main() -> None:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.display.set_caption("Music Player with Keyboard Controller")
    screen = pygame.display.set_mode((760, 500))
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("arial", 40, bold=True)
    font_body = pygame.font.SysFont("arial", 24)
    font_small = pygame.font.SysFont("arial", 20)

    music_dir = Path(__file__).parent / "music" / "sample_tracks"
    try:
        pygame.mixer.init()
        player = MusicPlayer(music_dir)
        audio_ready = True
    except Exception:
        # Fall back to a visual-only mode if audio hardware is unavailable.
        audio_ready = False
        player = None
        error_text = "Audio device is unavailable. The interface still works."

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif audio_ready and player is not None:
                    if event.key == pygame.K_p:
                        if player.status == "paused":
                            player.resume()
                        elif player.status == "playing":
                            player.pause()
                        else:
                            player.play()
                    elif event.key == pygame.K_s:
                        player.stop()
                    elif event.key == pygame.K_n:
                        player.next_track()
                    elif event.key == pygame.K_b:
                        player.previous_track()
            elif audio_ready and player is not None and event.type == player.endevent:
                player.next_track()

        screen.fill((245, 245, 250))

        title = font_title.render("Music Player", True, (25, 25, 25))
        screen.blit(title, (30, 25))

        if audio_ready and player is not None:
            track = player.current
            status = player.status.capitalize()
            duration = fmt_time(track.duration or 0)
            pos = fmt_time(player.progress_seconds())
            ratio = player.progress_ratio()

            screen.blit(font_body.render(f"Track: {track.name}", True, (30, 30, 30)), (30, 100))
            screen.blit(font_body.render(f"Status: {status}", True, (30, 30, 30)), (30, 140))
            screen.blit(font_body.render(f"Position: {pos} / {duration}", True, (30, 30, 30)), (30, 180))
            screen.blit(font_body.render(f"Playlist: {player.index + 1} / {len(player.tracks)}", True, (30, 30, 30)), (30, 220))

            draw_progress_bar(screen, 30, 280, 700, 28, ratio)

            controls = [
                "P - Play / Pause / Resume",
                "S - Stop",
                "N - Next track",
                "B - Previous track",
                "Q or Esc - Quit",
            ]
            for i, line in enumerate(controls):
                screen.blit(font_small.render(line, True, (70, 70, 70)), (30, 340 + i * 28))
        else:
            screen.blit(font_body.render(error_text, True, (170, 40, 40)), (30, 120))
            screen.blit(font_body.render("Install and run on a computer with audio support.", True, (50, 50, 50)), (30, 160))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
