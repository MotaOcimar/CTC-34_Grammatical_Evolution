import csv
import numpy
import sympy


class DataAnalyzer:

    def __init__(self, path):
        with open(path) as f:
            reader = csv.reader(f)
            next(reader)
            x = []
            self.data = []
            for row in reader:
                self.data.append(numpy.float_(row[1:9]))
                if len(row) == 10:
                    x.append(row[9])
            self.expected_strength = numpy.float_(x)
            #print(self.data)
            #print(self.expected_strength)

    def strength(self, exp):
        x1 = sympy.Symbol('x1')
        x2 = sympy.Symbol('x2')
        x3 = sympy.Symbol('x3')
        x4 = sympy.Symbol('x4')
        x5 = sympy.Symbol('x5')
        x6 = sympy.Symbol('x6')
        x7 = sympy.Symbol('x7')
        x8 = sympy.Symbol('x8')
        symbolic_exp = sympy.sympify(exp)
        strength = []
        for x in self.data:
            strength.append(symbolic_exp.subs({x1: x[0], x2: x[1], x3: x[2], x4: x[3], x5: x[4], x6: x[5], x7: x[6],
                                               x8: x[7]}))
        strength = numpy.array(strength)
        print(strength)
        strength = numpy.array(strength)
        return strength / numpy.max(strength)

    def mean_squared_error(self, exp):
        return numpy.square(numpy.subtract(self.strength(exp), self.expected_strength)).mean()
