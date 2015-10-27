__author__ = 'perar'
import json
import random

class TaskGenerator:

    def __init__(self):
        pass

    @staticmethod
    def load_tags():
        with open("tags.json", "r") as file:
            tags = json.loads(file.read())
        return tags

    @staticmethod
    def generate(count=50, even_split=False):

        tags = TaskGenerator.load_tags()

        # If self.even_split is True, split evenly the total self.count, Else use count for each of the tags
        number_of_tasks = int(count / len(tags)) if even_split else int(count)

        tasks = []

        for tag in tags:

            tag_name = tag["name"]
            tag_includes = tag["include"]

            for i in range(number_of_tasks):

                # Determine number of includes for this
                # Its a 40 % chance to include a sub-tag
                # If by chance the counter gets larger then number of defined includes:
                # Set counter to length of tag_includes
                count = 0
                rnd = random.randint(0, 100)
                while 0 < rnd <= 50:
                    count += 1
                    rnd = random.randint(0, 100)
                if count > len(tag_includes):
                    count = len(tag_includes)

                # Retrieve final include list
                final_includes = list(set(random.sample(tag_includes, count)))

                # Add task
                tasks.append({
                    "name": "{0}_Task_{1}".format(tag_name, str(i)),
                    "tag": tag_name,
                    "include": final_includes
                })

        print("Generated {0} tasks in {1} tags".format(str(len(tasks)), str(len(tags))))

        with open("tasks.json", "w") as file:
            file.write(json.dumps(tasks))


        return tasks

    @staticmethod
    def load():

        try:
            with open("tasks.json", "r") as file:
                tasks = json.loads(file.read())
                return tasks
        except:
            print("Error with tasks.json, Generating with default data...")
            TaskGenerator.generate()
            return TaskGenerator.load()





