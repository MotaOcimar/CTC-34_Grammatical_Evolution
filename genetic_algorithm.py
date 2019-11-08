import random
import numpy as np
from data_analyzer import *


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
        for i in range(1, self.population_size):
            self.population.append(random.sample(range(0, self.gene_max), self.chromosome_size))

    def proportionateSelection(self):
        probabilities = list()
        fitness = np.divide(1, self.MSE)
        fitness_sum = np.sum(fitness)
        previous_probability = 0.0

        for i in range(0, self.population_size - 1):
            probabilities.append(previous_probability + (fitness[i] / fitness_sum))

        rand = random.random()
        for subject in range(0, self.population_size-1):
            if rand < probabilities[subject]:
                return subject

    def crossover(self, parents):
        rand = random.randint(1, self.chromosome_size-1)
        bros = parents[0][0:rand] + parents[1][rand::]
        sis = parents[1][0:rand] + parents[0][rand::]
        return [bros, sis]

    def mutation(self, son, mutation_rate=0.1):
        for gene in range(0, self.chromosome_size-1):
            if random.random() < mutation_rate:
                son[gene] = random.randint(0, self.gene_max)
        for gene in range(0, self.chromosome_size - 1):
            if random.random() < mutation_rate:
                son[gene] = random.randint(0, self.gene_max)
        return son

    def evolve(self, grammar, filename, crossing_probability=0.8, mutation_rate=0.1, num_loops=1000,
               satisfactory_MSE=0.01):
        # Assessment:
        MSEcalculator = DataAnalyzer(filename)
        for chromosome in self.population:
            expr = grammar.derivateExpression(chromosome)
            self.MSE.append(MSEcalculator.mean_squared_error(expr))
        max_MSE = max(self.MSE)

        # Evolve loop
        generation = 0
        while generation < num_loops and max_MSE > satisfactory_MSE:
            # Selection, crossing and mutation:
            for parents_index in range(0, self.population_size//2-1):
                # Selection:
                parents = [self.proportionateSelection(), self.proportionateSelection()]
                rand = random.random()
                if rand < crossing_probability:
                    # Crossing:
                    children = self.crossover(parents)
                else:
                    # if it don't cross, just pass:
                    children = parents
                # Mutation:
                self.population[parents_index] = self.mutation(children[0], mutation_rate)
                self.population[parents_index+1] = self.mutation(children[1], mutation_rate)

            generation = generation+1
            # Assessment:
            # (Here due to the stopping criterion)
            for chromosome in self.population:
                expr = grammar.derivateExpression(chromosome)
                self.MSE.append(MSEcalculator.mean_squared_error(expr))
            max_MSE = max(self.MSE)

        # Population is returned ordered by MSE
        return [x for _, x in sorted(zip(self.MSE, self.population))]
