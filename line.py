class Line:
    def __init__(self, row: int, spawn_time: int, start_time: int, end_time: int, despawn_time: int):
        self.row = row
        self.spawn_time = spawn_time
        self.start_time = start_time
        self.end_time = end_time
        self.despawn_time = despawn_time