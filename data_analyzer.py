import csv
import numpy as np
from sklearn.metrics import mean_squared_error


class DataAnalyzer:

    def __init__(self, path):
        with open(path) as f:
            reader = csv.reader(f)
            next(reader)
            x = []
            self.data = []
            for row in reader:
                self.data.append(np.float_(row[1:9]))
                if len(row) == 10:
                    x.append(row[9])
            self.expected_strength = np.float_(x)

    def strength(self, exp):
        func = eval('lambda varA, varB, varC, varD, varE, varF, varG, varH:' + exp)
        strength_list = []
        for x in self.data:
            try:
                strength_list.append(func(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
            except:
                strength_list.append(np.nan)

        return strength_list

    def mean_squared_error(self, exp):
        try:
            return mean_squared_error(self.expected_strength, self.strength(exp))
        except:
            return np.nan
