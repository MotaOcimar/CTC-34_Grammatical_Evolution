from data_analyzer import DataAnalyzer
from genetic_algorithm import GeneticAlgorithm
from Grammar.Expression import Expression
import csv

# filename = "training.csv"
filename = 'just-sum.csv'
evolution = GeneticAlgorithm(population_size=100, chromosome_size=100)
evolution.createPopulation()
population = evolution.evolve(filename)

expr_gen = Expression(num_digits=8)
expr = expr_gen.derivateFromChromosome(population[0], 5)

analysis = DataAnalyzer(filename)
strength = analysis.strength(expr)

#print(analysis.strength('x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8'))
with open('sample.csv', mode='w') as f:
    sample_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sample_writer.writerow(['ID', 'strength'])
    i = 722
    for value in strength:
        sample_writer.writerow([i, value])
