class Cell:
    def __init__(self):
        self.reset()

    def reset(self):
        self.open = False
        self.mine = False
        self.border = 0
        self.current = False
        self.flag = False
