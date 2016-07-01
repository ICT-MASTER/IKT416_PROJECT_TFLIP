__author__ = 'perar'

import matplotlib.pyplot as plt
import math
import Validation.StudentRegression as StudentRegression
import Validation.StaticEpsilonPercent as StaticEpsilonPercent
import Validation.StudentSkillComparion as StudentSkillComparion

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

if __name__ == '__main__':

    """a = []
    b = []
    for n in drange(-2.5, 2.5, .01):
        print(n)
        y = (1 * math.pow(n, 2)) + 0.5
        a.append(n)
        b.append(y)


    plt.plot(a,b)
    plt.xlabel('Skill Difference/Distance')
    plt.ylabel('Beta factor')
    plt.grid(False)
    plt.show()"""


    #StudentSkillComparion.run(100, 100, 100)


    StudentRegression.run(100, 1000)

    # Good Student
    StaticEpsilonPercent.run(100, 1000, .70)

    # Bad Student
    StaticEpsilonPercent.run(100, 1000, .20)






