import os

def experience_formula(level):
    return (level + 1) * 2




# Function to retrieve all student data (from file)
def get_students():

    data = {}

    student_directory = "./Students"

    for student in os.listdir(student_directory):
        data[student] = {
            'level': 0,
            'experience': 10,
            'next_level': experience_formula(0),  # 0 = Level
            'tags': [
                {
                    'tag': 'if',
                    'level': 1,
                    'failed': 2,
                    'total': 5
                },
                {
                    'tag': 'while',
                    'level': 0,
                    'failed': 3,
                    'total': 3
                }
            ]

        }

    return data
