import random


class GeneticAlgorithm:
    population = list()
    fitness = list()

    def __init__(self, population_size, chromosome_size, gene_max, num_loops, grammar):
        # Constantes:
        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.gene_max = gene_max
        self.num_loops = num_loops

    def createPopulation(self):
        # Cria a polulação:
        for i in range(1, self.population_size):
            self.population.append(random.sample(range(0, self.gene_max), self.chromosome_size))

    def evolve(self):
        # Loop de evolução
        for i in range(1, self.num_loops):

            # para cada indivíduo
            self.grammar.fitness()

