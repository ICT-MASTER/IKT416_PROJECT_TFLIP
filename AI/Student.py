__author__ = 'perar'




class Student:

    def __init__(self, skill):

        if skill < 0 or skill > 1:
            raise ValueError('Skill should be between 0 and 1')

        self.skill = skill


    ######
    ##
    ## Get assignment, fetches a assignment from the Automata
    ##
    ##
    #####
    def get_assignment(self):
        return self


