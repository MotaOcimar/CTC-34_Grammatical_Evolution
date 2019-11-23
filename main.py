from data_analyzer import DataAnalyzer
from genetic_algorithm import GeneticAlgorithm
import numpy as np
import csv

file_training = "training.csv"
# file_training = 'just_sum.csv'
evolution = GeneticAlgorithm(population_size=10000, chromosome_size=65)
evolution.createPopulation()
total_generations = evolution.evolve(file_training, crossing_probability=1, mutation_rate=0.1, plague_max_percent=0.4,
                                     plague_probability=0.1, selection_exp_const=1, min_num_vars=3,
                                     max_generations=200, const_num_digits=3, satisfactory_mse=0.01)

print("\n\n\nBest subject: ", evolution.best_expr)
print("sqrt(MSE): ", np.sqrt(min(evolution.mse_list)))
print("In ", total_generations, "generations")

analysis = DataAnalyzer('testing.csv')
strength = analysis.strength(evolution.best_expr)

with open('sub0.csv', mode='w') as f:
    sample_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sample_writer.writerow(['ID', 'strength'])
    i = 722
    for value in strength:
        sample_writer.writerow([i, value])
        i += 1
