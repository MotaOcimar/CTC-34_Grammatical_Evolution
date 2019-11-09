from data_analyzer import DataAnalyzer
from genetic_algorithm import GeneticAlgorithm
import csv

filename = "training.csv"
evolution = GeneticAlgorithm()
evolution.createPopulation()
population = evolution.evolve(filename)
analysis = DataAnalyzer(filename)

strength = analysis.strength(population[0])

#print(analysis.strength('x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8'))
with open('sample.csv', mode='w') as f:
    sample_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sample_writer.writerow(['ID', 'strength'])
    i = 722
    for value in strength:
        sample_writer.writerow([i, value])
