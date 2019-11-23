import random
import bisect
from collections import Counter
from Grammar.Expression import Expression
from data_analyzer import *


class GeneticAlgorithm:
    population = list()
    mse_list = list()
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
            self.population.append([random.randint(0, self.gene_max) for j in range(0, self.chromosome_size)])

    def expProportionateSelection(self, selection_exp_const=50):
        probabilities = []
        fitness = list(np.exp(np.divide(selection_exp_const*self.min_mse, self.mse_list))-1)
        # the '-1' is to fitness(mse = inf) = 0

        fitness_sum = np.sum(fitness)
        previous_probability = 0.0

        for i in range(0, self.population_size):
            previous_probability = previous_probability + (fitness[i] / fitness_sum)
            probabilities.append(previous_probability)

        rand = random.random()
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

    def plague(self, plague_max_percent=0.5, plague_exact_percent=None):
        if plague_exact_percent is None:
            rand = random.random()*plague_max_percent
            percent = (self.population_size*rand)/self.population_size
        else:
            percent = plague_exact_percent

        print("\nOHH NO!!! The black plague came and wiped out about ",
              round(percent*100, 4), "% of the population!", sep='')

        for i in range(0, int(self.population_size*percent)):
            rand_index = random.randint(0, self.population_size-1)
            self.population[rand_index] = [random.randint(0, self.gene_max) for j in range(0, self.chromosome_size)]

    def evaluation(self, mse_calculator, expr_gen, min_num_vars=3, satisfactory_mse=10**-6):
        self.mse_list = []
        expr_list = []
        useful_size_list = []
        self.min_mse = np.inf
        self.best_expr = None

        for chromosome in self.population:
            expr_gen.reset()
            expr = expr_gen.derivateFromChromosome(chromosome, 5)
            if expr.count("var") < min_num_vars:
                mse = np.inf
            else:
                mse = round(mse_calculator.mean_squared_error(expr), 10)

            # to avoid nan/inf fitness:
            if not np.isfinite(mse):
                mse = np.inf
            elif mse == 0:
                mse = satisfactory_mse

            # finding the best expression:
            if mse < self.min_mse:
                self.min_mse = mse
                self.best_expr = expr

            self.mse_list.append(mse)
            expr_list.append(expr)
            useful_size_list.append(expr_gen.useful_size)

        mse_sorted = self.mse_list.copy()
        mse_sorted.sort()

        print("OK\n\nTop 5:")
        next_index = 0
        for i in range(0, 5):
            num_occurrence = mse_sorted.count(mse_sorted[next_index])
            print("\n\t\t #", i+1, ":\t", expr_list[self.mse_list.index(mse_sorted[next_index])], sep='')
            print("\t\tsqrt(MSE):", np.sqrt(mse_sorted[next_index]),
                  "\tUseful size:", useful_size_list[self.mse_list.index(mse_sorted[next_index])],
                  "\tFrequency:", num_occurrence)
            next_index += num_occurrence
            if next_index >= self.population_size:
                break

        aux = [x for x in mse_sorted if np.isfinite(x)]
        data = Counter(aux)
        mode_mse = data.most_common(1)[0][0]
        print("\n\t\tMost frequent (and fertile):\n\t\t\t\t", expr_list[self.mse_list.index(mode_mse)], sep='')
        print("\t\tsqrt(MSE):", np.sqrt(mode_mse),
              "\tUseful size:", useful_size_list[self.mse_list.index(mode_mse)],
              "\tFrequency:", self.mse_list.count(mode_mse))

    def evolve(self, filename, crossing_probability=0.8, mutation_rate=0.1, plague_probability=0.1,
               plague_max_percent=0.5, plague_exact_percent=None, selection_exp_const=50, max_generations=200,
               min_num_vars=3, const_num_digits=3, satisfactory_mse=10**-6):
        # Evaluation:
        print("Generation 1: Evaluating...")
        mse_calculator = DataAnalyzer(filename)
        expr_gen = Expression(const_num_digits)
        self.evaluation(mse_calculator, expr_gen, min_num_vars, satisfactory_mse)

        # Evolve loop:
        generation = 1
        while generation < max_generations and min(self.mse_list) > satisfactory_mse:

            # Plague:
            if random.random() < plague_probability:
                self.plague(plague_max_percent, plague_exact_percent)

            # Selection, crossing and mutation:
            print("\n\nSelecting and crossing ...", end="")
            for children_index in range(0, self.population_size//2):
                # Selection:
                parents_index = [self.expProportionateSelection(selection_exp_const),
                                 self.expProportionateSelection(selection_exp_const)]
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
            print("OK\nGeneration " + str(generation)+": Evaluating...", end="")

            self.evaluation(mse_calculator, expr_gen, min_num_vars, satisfactory_mse)

        return generation
