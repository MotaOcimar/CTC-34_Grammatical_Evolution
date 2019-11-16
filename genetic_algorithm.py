import random
import bisect
from Grammar.Expression import Expression
from data_analyzer import *


class GeneticAlgorithm:
    population = list()
    MSE = list()
    best_expr = None
    min_mse = np.inf

    def __init__(self, population_size=1000, chromosome_size=1000, gene_max=255):
        # Constantes:
        self.population_size = 2*(population_size//2)  # must be even
        self.chromosome_size = chromosome_size
        self.gene_max = gene_max

    def createPopulation(self):
        # Cria a polulação:
        for i in range(0, self.population_size):
            self.population.append([random.randint(0, self.gene_max) for i in range(0, self.chromosome_size)])

    def proportionateSelection(self):
        probabilities = []
        fitness = np.divide(1, self.MSE)
        fitness_sum = np.sum(fitness)
        previous_probability = 0.0

        for i in range(0, self.population_size):
            previous_probability = previous_probability + (fitness[i] / fitness_sum)
            probabilities.append(previous_probability)

        # print(fitness_sum)
        # print(probabilities)
        rand = random.random()
        # print(rand)
        return bisect.bisect_left(probabilities, rand)

    def expProportionateSelection(self, selection_exp_const=50):
        probabilities = []
        fitness = list(np.exp(np.divide(selection_exp_const*self.min_mse, self.MSE))-1)  # the '-1' is to fitness(mse = inf) == 0

        fitness_sum = np.sum(fitness)
        previous_probability = 0.0

        for i in range(0, self.population_size):
            previous_probability = previous_probability + (fitness[i] / fitness_sum)
            probabilities.append(previous_probability)

        # print(fitness_sum)
        # print(probabilities)
        rand = random.random()
        # print(rand)
        return bisect.bisect_left(probabilities, rand)

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

    def evaluation(self, MSEcalculator, expr_gen, satisfactory_MSE=10**-6):
        self.MSE = []
        self.min_mse = np.inf
        self.best_expr = None
        useful_size = None

        for chromosome in self.population:
            expr_gen.reset()
            expr = expr_gen.derivateFromChromosome(chromosome, 5)
            mse = MSEcalculator.mean_squared_error(expr)

            # to avoid nan/inf fitness:
            if not np.isfinite(mse):
                mse = np.inf
            elif mse == 0:
                mse = satisfactory_MSE

            # finding the best expression:
            if mse < self.min_mse:
                self.min_mse = mse
                self.best_expr = expr
                useful_size = expr_gen.useful_size
            # print(expr, ": ", mse)
            self.MSE.append(mse)

        print(self.best_expr, "\t\tsqrt(MSE): ", np.sqrt(self.min_mse), "\t\tUseful size: ", useful_size)

    def evolve(self, filename, crossing_probability=0.8, mutation_rate=0.1, selection_exp_const=50, max_generations=200,
               const_num_digits=3, satisfactory_MSE=10**-6):
        # Evaluation:
        print("Generation 1: Evaluation")
        MSEcalculator = DataAnalyzer(filename)
        expr_gen = Expression(const_num_digits)
        self.evaluation(MSEcalculator, expr_gen, satisfactory_MSE)

        # Evolve loop:
        generation = 1
        while generation < max_generations and min(self.MSE) > satisfactory_MSE:
            # Selection, crossing and mutation:
            # print("\n\nGeneration ", generation, ": Selection and crossing")
            for children_index in range(0, self.population_size//2):
                # Selection:
                parents_index = [self.expProportionateSelection(selection_exp_const),
                                 self.expProportionateSelection(selection_exp_const)]
                # print(parents_index)
                rand = random.random()
                if rand < crossing_probability:
                    # Crossing:
                    children = self.crossover(parents_index)
                else:
                    # if it don't cross, just pass:
                    children = [self.population[parents_index[0]], self.population[parents_index[1]]]
                # Mutation:
                self.population[2*children_index] = self.mutation(children[0], mutation_rate)
                self.population[2*children_index+1] = self.mutation(children[1], mutation_rate)

            generation = generation+1
            # Evaluation:
            # (Here due to the stopping criterion)
            print("\n\nGeneration ", generation, ": Evaluation")
            self.evaluation(MSEcalculator, expr_gen, satisfactory_MSE)

        # self.best_subject_index = self.MSE.index(min(self.MSE))
        # self.best_subject = self.population[self.best_subject_index]

        return generation
