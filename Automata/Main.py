from __future__ import print_function

# Libraries
import sys
import operator
import sys
import time


# Internal classes
from Automata import Automata
from Environment import Environment


# Initial argument parsing
states = 3
num_automata = 5
iterations = 1000
times = 1000


arguments = sys.argv[1:]

if len(arguments) > 0:
    states = arguments[0]

if len(arguments) > 1:
    num_automata = arguments[1]

if len(arguments) > 2:
    iterations = arguments[2]

if len(arguments) > 3:
    times = arguments[3]

print("Mega advanced automata is initiating...")
print("Using following parameters:")
print("-------")
print("States: {0}\nAutomatas: {1}\nIterations: {2}\nLoops: {3}".format(states, num_automata, iterations, times))
print("-------")
print("Progress: ")


startTime = time.time()

# Create automatas
automata_list = [Automata(states) for x in range(num_automata)]
result = {}


for x in range(times):
    for x in range(iterations):

        # Count yes for each of the automatas
        yes = 0
        for automata in automata_list:
            yes = yes + 1 if automata.isYes() else yes

    # Create environment and calculate probability
    env = Environment(yes, len(automata_list))
    env.probability()

    # Determine weither to punish or reward automatas
    for automata in automata_list:
        automata.reward() if env.doReward() else automata.punish()

    # Generate key for Dict result (IE: 3/2)
    result_key = "{0}/{1}".format(yes, len(automata_list) - yes)

    # Ensure that the key exist, init if not.
    result[result_key] = 1 if result_key not in result else result[result_key] + 1

    out = ""
    for key, value in sorted(result.items(), key=operator.itemgetter(1), reverse=True):
        out = out + "[" + (key+ ": " + str(value)) + "]\t"

    print(out, end="\r")

    #open('data.dat', 'w').close()
    #for key, value in sorted(result.items(), key=operator.itemgetter(1), reverse=True):
    #print("{0}: {1}").format(key, value)
    #    with open ('data.dat', 'a') as f: f.write (key+ "   " + str(value) + '\n')
        #os.system("python termgraph.py data.dat")

endTime = time.time()


print("\nExecuted in {0} seconds.".format(endTime - startTime))