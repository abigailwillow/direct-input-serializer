from pathlib import Path

class AudioTracks:
    def __init__(self, *, preview: Path, instrumentals: Path, vocals: Path):
        self.preview = preview
        self.instrumentals = instrumentals
        self.vocals = vocals