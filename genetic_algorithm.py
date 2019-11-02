import random
import numpy as np


class GeneticAlgorithm:
    population = list()
    fitness = list()

    def __init__(self, population_size = 1000, chromosome_size = 10, gene_max = 255, num_loops = 100):
        # Constantes:
        self.population_size = population_size
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

        for i in range(self.population_size):
            probabilities.append(previous_probability + (self.fitness[i] / fitness_sum))

        rand = random.random()
        for subject in range(0, self.population_size-1):
            if rand < probabilities[subject]:
                return subject

    def evolve(self, grammar):
        # Loop de evolução
        for i in range(1, self.num_loops):

            # Avaliação:
            for chromosome in self.population:
                expr = grammar.derivateExpression(chromosome)
                self.fitness.append(1.0/grammar.cost(expr))

            # Seleção:
            selected_chromosomes = list
            # for i in range(1,10)

