from Grammar.Expression import Expression
import numpy as np

expression = Expression(5)

chromosome = [8, 53, 54, 56, 456, 54, 34, 3, 8, 39, 7]

formula = expression.derivateFromChromosome(chromosome, 5)

print(formula)
a = 1
b = 2
c = 3
d = 4
e = 5
f = 6
g = 7
h = 8
print(eval(formula))