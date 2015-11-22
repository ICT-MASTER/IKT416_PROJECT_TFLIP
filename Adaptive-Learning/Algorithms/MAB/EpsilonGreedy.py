import random


def ind_max(arms):

    highest = None
    for arm in arms:
        if highest is None:
            highest = arm
        elif highest.value < arm.value:
            highest = arm

    return arms.index(highest)


class EpsilonGreedy():
    def __init__(self, epsilon = 0.1):
        self.epsilon = epsilon
        self.arms = []
        return

    def initialize(self, arms):
        self.arms = arms
        return

    def select_arm(self):
        if random.random() > self.epsilon:
            return ind_max(self.arms)  # Select highest value arm
        else:
            return random.randrange(len(self.arms))  # Select random arm

    def update(self, chosen_arm, reward):
        chosen_arm = min(len(self.arms)-1, chosen_arm + 1)


        # Increase count on chosen arm
        self.arms[chosen_arm].count = self.arms[chosen_arm].count + 1

        n = self.arms[chosen_arm].count
        value = self.arms[chosen_arm].value

        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward

        self.arms[chosen_arm].value = new_value

        return
