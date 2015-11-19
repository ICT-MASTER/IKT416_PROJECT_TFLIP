__author__ = 'Per-Arne'
import random

class Environment(object):

    def __init__(self, yes, num_automatas):
        self.yes = yes # M
        self.num_automatas = num_automatas
        self.prob = 0


    def probability(self):

        percent_yes = (self.yes / self.num_automatas) * 100.0

        # Above 60% YES
        if percent_yes <= 60:
            self.prob = self.yes * 0.2  # yes=5, probl =1 ... yes=0, prob = 0,
        else:
            self.prob = 0.6 - (self.yes - 3) * 0.2  # yes=5, 0.6-2*0.2 = 0.5


    def doReward(self):

        r_num = random.uniform(0.0, 1.0)

        if r_num >= self.prob:
            return False
        else:
            return True
