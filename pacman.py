class Pacman:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.mouthOpen = False
        self.pacSpeed = 1/4
        self.mouthChangeDelay = 5
        self.mouthChangeCount = 0
        self.dir = 'up'
        self.newDir = 'up'

    def update(self):
        pass