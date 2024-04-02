from pathlib import Path
from models import AudioTracks

class Settings:
    def __init__(self, title: str, disc_sticker: Path, splash: Path, audio_tracks: AudioTracks, notes_for_cutscene: int, cutscene_start: int, cutscene_end: int, cutscene_pre_rendered: Path, great_timing: float = 0.1, good_timing: float = 0.2):
        self.title = title
        self.disc_sticker = disc_sticker
        self.splash = splash
        self.audio_tracks = audio_tracks
        self.notes_for_cutscene = notes_for_cutscene
        self.cutscene_start = cutscene_start
        self.cutscene_end = cutscene_end
        self.cutscene_pre_rendered = cutscene_pre_rendered
        self.great_timing = great_timing
        self.good_timing = good_timing