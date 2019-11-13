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
            #print(self.data)
            #print(self.expected_strength)

    def strength(self, exp):
        # symbolic_exp = sympy.sympify(exp)
        func = eval('lambda a, b, c, d, e, f, g, h:' + exp)
        strength = []
        for x in self.data:
            try:
                strength.append(func(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
            except:
                strength.append(np.nan)

        return strength

    def oldstrength(self, exp):
        # symbolic_exp = sympy.sympify(exp)
        strength = []
        for x in self.data:
            a = x[0]
            b = x[1]
            c = x[2]
            d = x[3]
            e = x[4]
            f = x[5]
            g = x[6]
            h = x[7]
            try:
                strength.append(eval(exp))
            except:
                strength.append(np.nan)
        strength = np.array(strength)
        #print(strength)
        return strength #/ np.max(strength)

    def mean_squared_error(self, exp):
        try:
            return mean_squared_error(self.expected_strength, self.strength(exp))
        except:
            return np.nan

    def old_mean_squared_error(self, exp):
        return sum(np.square(np.subtract(self.oldstrength(exp), self.expected_strength)))/(len())
