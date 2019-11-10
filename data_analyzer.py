
import csv
import numpy as np
import sympy


class DataAnalyzer:
    # x1 = sympy.Symbol('x1')
    # x2 = sympy.Symbol('x2')
    # x3 = sympy.Symbol('x3')
    # x4 = sympy.Symbol('x4')
    # x5 = sympy.Symbol('x5')
    # x6 = sympy.Symbol('x6')
    # x7 = sympy.Symbol('x7')
    # x8 = sympy.Symbol('x8')

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
            # strength.append(symbolic_exp.subs({self.x1: x[0], self.x2: x[1], self.x3: x[2], self.x4: x[3],
            #                                    self.x5: x[4], self.x6: x[5], self.x7: x[6], self.x8: x[7]}))
        # strength = np.array(strength)
        #print(strength)
        return strength #/ np.max(strength)

    def mean_squared_error(self, exp):
        return np.square(np.subtract(self.strength(exp), self.expected_strength)).mean()
