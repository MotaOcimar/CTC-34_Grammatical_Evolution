import csv
import numpy
import sympy


class MSECalculator:

    def __init__(self):
        with open('training.csv') as f:
            reader = csv.reader(f)
            next(reader)
            x = []
            self.data = []
            for row in reader:
                self.data.append(numpy.float_(row[1:len(row)-1]))
                x.append(row[len(row)-1])
            self.expected_value = numpy.float_(x)

    def mean_squared_error(self, exp):
        x1 = sympy.Symbol('x1')
        x2 = sympy.Symbol('x2')
        x3 = sympy.Symbol('x3')
        x4 = sympy.Symbol('x4')
        x5 = sympy.Symbol('x5')
        x6 = sympy.Symbol('x6')
        x7 = sympy.Symbol('x7')
        x8 = sympy.Symbol('x8')
        symbolic_exp = sympy.sympify(exp)
        value = []
        for x in self.data:
            value.append(symbolic_exp.subs({x1: x[0], x2: x[1], x3: x[2], x4: x[3], x5: x[4], x6: x[5], x7: x[6],
                                            x8: x[7]}))
        #print(value)
        value = numpy.array(value)
        value /= numpy.max(value)
        return numpy.square(numpy.subtract(value, self.expected_value)).mean()
