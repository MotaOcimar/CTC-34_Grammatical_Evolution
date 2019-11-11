from data_analyzer import DataAnalyzer
from genetic_algorithm import GeneticAlgorithm
import csv

filename = "training.csv"
# filename = 'just_x1+x2.csv'
evolution = GeneticAlgorithm(population_size=1000, chromosome_size=50)
evolution.createPopulation()
total_generations = evolution.evolve(filename, crossing_probability=1, mutation_rate=0.1, max_generations=100)

print("\n\n\nBest subject: ", evolution.best_expr)
print("MSE: ", min(evolution.MSE))
print("In ", total_generations, "generations")

analysis = DataAnalyzer('testing.csv')
strength = analysis.strength(evolution.best_expr)

with open('sample.csv', mode='w') as f:
    sample_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sample_writer.writerow(['ID', 'strength'])
    i = 722
    for value in strength:
        sample_writer.writerow([i, value])
        i += 1
