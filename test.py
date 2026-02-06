import csv
import random

with open("shortjokes.csv", mode="r", encoding="utf-8") as file:
        #line_count = sum(1 for line in file)
        #print(line_count)
        reader = csv.DictReader(file)

        data_list = []

        for row in reader:
            data_list.append(row)

        print(len(data_list))
        #for data in data_list:
        #    print(data)


        print(f"Joke: {data_list[random.randint(0, len(data_list) - 1)]["Joke"]}")