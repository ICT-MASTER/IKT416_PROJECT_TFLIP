__author__ = 'perar'
from Automata.MAB.EpsilonGreedy import EpsilonGreedy
from Automata.MAB.Arm import Arm



tags = {
    'Level 1': 1.0,
    'Level 2': 0.5,
    'Level 3': 0.25,
    'Level 4': 0.125,
    'Level 5': 0,
    'Level 6': 0,
    'Level 7': 0,
    'Level 8': 0,
    'Level 9': 0,
    'Level 10': 0
}
arms = []

for key in tags:
    arm = Arm(key, tags[key])
    arm.value = 0 #tags[key]
    arms.append(arm)

# Initialize Bandit
eps = EpsilonGreedy(0.1)
eps.initialize(arms)


iterations = 100

# Run 1000 iterations
for t in range(iterations):
    chosen_arm = eps.select_arm()
    reward = arms[chosen_arm].draw()
    eps.update(chosen_arm, reward)


for arm in arms:
    percent = (arm.count / iterations) * 100
    print("{0}: {1} - {2}%\t|{3}|".format(arm.tag, arm.count,int(percent), ''.join(["-" for x in range(int(percent))])))

