import random
import numpy as np
from data_analyzer import *


class GeneticAlgorithm:
    population = list()
    fitness = list()

    def __init__(self, population_size = 1000, chromosome_size = 10, gene_max = 255, num_loops = 100):
        # Constantes:
        self.population_size = 2*(population_size//2) # must be even
        self.chromosome_size = chromosome_size
        self.gene_max = gene_max
        self.num_loops = num_loops

    def createPopulation(self):
        # Cria a polulação:
        for i in range(1, self.population_size):
            self.population.append(random.sample(range(0, self.gene_max), self.chromosome_size))

    def proportionateSelection(self):
        probabilities = list()
        fitness_sum = np.sum(self.fitness)
        previous_probability = 0.0

        for i in range(0, self.population_size - 1):
            probabilities.append(previous_probability + (self.fitness[i] / fitness_sum))

        rand = random.random()
        for subject in range(0, self.population_size-1):
            if rand < probabilities[subject]:
                return subject

    def crossover(self, parents):
        rand = random.randint(1, self.chromosome_size-1)
        bros = parents[0][0:rand] + parents[1][rand::]
        sis = parents[1][0:rand] + parents[0][rand::]
        return [bros, sis]

    def mutation(self, son, mutation_rate = 0.1):
        for gene in range(0, self.chromosome_size-1):
            if random.random() < mutation_rate:
                son[gene] = random.randint(0, self.gene_max)
        for gene in range(0, self.chromosome_size - 1):
            if random.random() < mutation_rate:
                son[gene] = random.randint(0, self.gene_max)
        return son

    def evolve(self, grammar, crossing_probability=0.8, mutation_rate=0.1):
        # Loop de evolução
        for generation in range(1, self.num_loops):

            # Assessment:
            MSEcalculator = DataAnalyzer('training.csv')
            for chromosome in self.population:
                expr = grammar.derivateExpression(chromosome)
                self.fitness.append(1.0/MSEcalculator.mean_squared_error(expr))

            # Selection, crossing and mutation:
            for parents_index in range(0, self.population_size//2-1):
                # Selection:
                parents = [self.proportionateSelection(), self.proportionateSelection()]
                rand = random.random()
                # Crossing:
                if rand < crossing_probability:
                    children = self.crossover(parents)
                    # Mutation:
                    self.population[parents_index] = self.mutation(children[0], mutation_rate)
                    self.population[parents_index+1] = self.mutation(children[1], mutation_rate)
                else:
                    # if it don't cross, just mutate:
                    self.population[parents_index] = self.mutation(parents[0], mutation_rate)
                    self.population[parents_index + 1] = self.mutation(parents[1], mutation_rate)

        return self.population # [x for _, x in sorted(zip(fitness,self.population))]


