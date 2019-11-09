import random
import numpy as np
from Expression import Expression
from data_analyzer import *

# TODO: Ajustar ranges dos FORS

class GeneticAlgorithm:
    population = list()
    MSE = list()

    def __init__(self, population_size=1000, chromosome_size=10, gene_max=255):
        # Constantes:
        self.population_size = 2*(population_size//2)  # must be even
        self.chromosome_size = chromosome_size
        self.gene_max = gene_max

    def createPopulation(self):
        # Cria a polulação:
        for i in range(0, self.population_size):
            self.population.append([random.randint(0, self.gene_max) for i in range(0, self.chromosome_size)])

    def proportionateSelection(self):
        probabilities = list()
        fitness = np.divide(1, self.MSE)
        fitness_sum = np.sum(fitness)
        previous_probability = 0.0

        for i in range(0, self.population_size):
            previous_probability = previous_probability + (fitness[i] / fitness_sum)
            probabilities.append(previous_probability)

        rand = random.random()
        for subject in range(0, self.population_size):
            if rand <= probabilities[subject]:
                return subject

        return self.population_size-1

    def crossover(self, parents_index):
        rand = random.randint(1, self.chromosome_size-1)
        bros = self.population[parents_index[0]][0:rand] + self.population[parents_index[1]][rand::]
        sis = self.population[parents_index[1]][0:rand] + self.population[parents_index[0]][rand::]
        return [bros, sis]

    def mutation(self, son, mutation_rate=0.1):
        for gene_index in range(0, self.chromosome_size):
            if random.random() < mutation_rate:
                son[gene_index] = random.randint(0, self.gene_max)
        return son

    def evolve(self, filename, crossing_probability=0.8, mutation_rate=0.1, num_loops=10000,
               satisfactory_MSE=0.01):
        # Assessment:
        print("0: Assessment ")
        MSEcalculator = DataAnalyzer(filename)
        grammar = Expression()
        for chromosome in self.population:
            # expr = grammar.derivateFromChromosome(chromosome, 5)
            expr = "x1+x2+x3+x4"
            self.MSE.append(MSEcalculator.mean_squared_error(expr))
            # print(self.MSE)
        max_MSE = max(self.MSE)

        # Evolve loop
        generation = 0
        while generation < num_loops and max_MSE > satisfactory_MSE:
            # Selection, crossing and mutation:
            print(generation, ": Selection and crossing")
            for children_index in range(0, self.population_size//2):
                # Selection:
                parents_index = [self.proportionateSelection(), self.proportionateSelection()]
                print(parents_index)
                rand = random.random()
                if rand < crossing_probability:
                    # Crossing:
                    children = self.crossover(parents_index)
                else:
                    # if it don't cross, just pass:
                    children = [self.population[parents_index[0]], self.population[parents_index[1]]]
                # Mutation:
                self.population[children_index] = self.mutation(children[0], mutation_rate)
                self.population[children_index+1] = self.mutation(children[1], mutation_rate)

            generation = generation+1
            # Assessment:
            print(generation, ": Assessment")
            # (Here due to the stopping criterion)
            for chromosome in self.population:
                # expr = grammar.derivateExpression(chromosome)
                expr = "x1+x2+x3+x4"
                self.MSE.append(MSEcalculator.mean_squared_error(expr))
            max_MSE = max(self.MSE)

        # Population is returned ordered by MSE
        return [x for _, x in sorted(zip(self.MSE, self.population))]
