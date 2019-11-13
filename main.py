from data_analyzer import DataAnalyzer
from genetic_algorithm import GeneticAlgorithm
import csv

file_training = "training.csv"
# file_training = 'just_sum.csv'
evolution = GeneticAlgorithm(population_size=5000, chromosome_size=50)
evolution.createPopulation()
total_generations = evolution.evolve(file_training, crossing_probability=1, mutation_rate=0.1, max_generations=200,
                                     const_num_digits=3)

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
