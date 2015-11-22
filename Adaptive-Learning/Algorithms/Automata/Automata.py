__author__ = 'Per-Arne'
import random
import uuid


class Automata(object):


    def __init__(self, states):

        # Do not allow odd numbers (Should never happen unless 3.5 example)
        if (states * 2) %  2 != 0:
            raise ValueError("Cannot use a odd number")

        self.states = states
        self.state = random.randint(self.states, (self.states) + 1)
        self.id = uuid.uuid1()
        # print("Automata: {0} - Init state: {1}").format(self.id, self.state)


        self.tmpyes = 0
        self.tmpno = 0


    def isYes(self):
        total_states = self.states * 2
        if self.state > (total_states / 2):
            return True
        else:
            return False


    def reward(self):

        total_states = self.states * 2

        # Positive side
        if self.state > (total_states / 2):
            #print ("Reward {0} --> {1}").format(self.state, min(self.state + 1, total_states))
            self.state = min(self.state + 1, total_states)
        # Negative side
        else:
            #print ("Reward {0} --> {1}").format(self.state, max(self.state - 1, 1))
            self.state = max(self.state - 1, 1)

    def punish(self):
        total_states = self.states * 2
        # Positive side
        if self.state > (total_states / 2):
            #print ("Punish {0} --> {1}").format(self.state, self.state - 1)
            self.state = self.state - 1
        # Negative side
        else:
            #print ("Punish {0} --> {1}").format(self.state, self.state + 1)
            self.state = self.state + 1

