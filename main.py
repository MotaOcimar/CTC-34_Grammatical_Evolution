import random


# Constantes:
population_size = 1000
chromosome_size = 10
gene_max = 255


# Cria a polulação:
population = list()
for i in range(1, population_size):
    population.append(random.sample(range(0, gene_max), chromosome_size))



