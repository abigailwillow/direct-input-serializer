from pathlib import Path

class Line:
    def __init__(self, *, row: int, spawn_time: float, start_time: float, end_time: float, despawn_time: float, lyric_width: float = 1, lyric_texture: Path = ''):
        self.row = row
        self.spawn_time = spawn_time
        self.start_time = start_time
        self.end_time = end_time
        self.despawn_time = despawn_time
        self.lyric_width = lyric_width
        self.lyric_texture = lyric_texture
