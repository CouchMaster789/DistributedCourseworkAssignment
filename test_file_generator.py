import random

length = 1024

with open("test_file_5.csv", "w") as file:
    for i in range(1, length + 1):
        line = ""

        for j in range(1, length + 1):
            line += str(random.randint(1, 1024)) + " "

        file.write(line[:-1] + "\n" if i < length else line[:-1])
