__author__ = 'perar'



class AssignmentGenerator:

    def __init__(self, count=50, tags=[], even_split=True):

        # Number of generated Assignments
        self.count = count

        # List of tags
        # Tag Format
        # {
        #   "name": "for",
        #   "include": []
        # },
        # {
        #   "name": "mvc",
        #   "include": ["for", "while", "if"]
        # },
        #
        self.tags = tags

        # Split assignments evenly on tags
        self.even_split = even_split

    def generate(self):

        # If self.even_split is True, split evenly the total self.count, Else use count for each of the tags
        number_of_assignments = int(self.count / len(self.tags)) if self.even_split else int(self.count)

        assignments = []

        for __ in self.tags:
            for i in range(number_of_assignments):

                assignments.append({
                    "name": "Assignment_{0}".format(str(i))
                })






