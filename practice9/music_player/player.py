from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import wave

import pygame


@dataclass
class TrackInfo:
    path: Path
    name: str
    duration: float | None


class MusicPlayer:
    def __init__(self, music_dir: str | Path) -> None:
        self.music_dir = Path(music_dir)
        self.tracks = self._load_tracks()
        if not self.tracks:
            raise RuntimeError(f"No audio files found in {self.music_dir}")

        self.index = 0
        self.status = "stopped"
        self.endevent = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.endevent)
        self._started_ms: int = 0

    def _load_tracks(self) -> list[TrackInfo]:
        files = []
        for ext in ("*.wav", "*.mp3", "*.ogg"):
            files.extend(sorted(self.music_dir.glob(ext)))

        tracks: list[TrackInfo] = []
        for path in files:
            tracks.append(TrackInfo(path=path, name=path.stem, duration=self._get_duration(path)))
        return tracks

    @staticmethod
    def _get_duration(path: Path) -> float | None:
        if path.suffix.lower() == ".wav":
            with wave.open(str(path), "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return frames / float(rate)
        return None

    @property
    def current(self) -> TrackInfo:
        return self.tracks[self.index]

    def _load_current(self) -> None:
        pygame.mixer.music.load(str(self.current.path))

    def play(self) -> None:
        self._load_current()
        pygame.mixer.music.play()
        self.status = "playing"
        self._started_ms = pygame.time.get_ticks()

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self.status = "stopped"

    def pause(self) -> None:
        pygame.mixer.music.pause()
        self.status = "paused"

    def resume(self) -> None:
        pygame.mixer.music.unpause()
        self.status = "playing"

    def next_track(self) -> None:
        self.index = (self.index + 1) % len(self.tracks)
        self.play()

    def previous_track(self) -> None:
        self.index = (self.index - 1) % len(self.tracks)
        self.play()

    def progress_seconds(self) -> float:
        if self.status != "playing":
            return 0.0
        return max(0.0, (pygame.time.get_ticks() - self._started_ms) / 1000.0)

    def progress_ratio(self) -> float:
        duration = self.current.duration
        if not duration:
            return 0.0
        return min(1.0, self.progress_seconds() / duration)
