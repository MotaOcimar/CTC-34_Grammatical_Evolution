import csv

class Trainer:

    def __init__(self):
        with open('training.csv') as f:
            reader = csv.reader(f)
            next(reader)
            self.data = []
            for row in reader:
                del row[0]
                self.data.append(row)
            print(self.data)

