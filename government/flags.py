class Flag:
    def __init__(self):
        pass


class NotEnoughHaliteFlag(Flag):
    def __init__(self, missing_halite):
        super().__init__()
        self.missing_halite = missing_halite
