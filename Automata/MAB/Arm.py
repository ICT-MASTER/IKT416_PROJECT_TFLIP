import random

class Arm:

    def __init__(self, tag, p):
        self.tag = tag  # The tag IE: if, while
        self.value = 0.0
        self.count = 0

        self.p = p

    def draw(self):
        if random.random() > self.p:
            return 0.0
        else:
            return 1.0
