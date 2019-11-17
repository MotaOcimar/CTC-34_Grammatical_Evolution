import random
import bisect
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

    def proportionateSelection(self):
        probabilities = []
        fitness = np.divide(1, self.mse_list)
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
        fitness = list(np.exp(np.divide(selection_exp_const*self.min_mse, self.mse_list))-1)
        # the '-1' is to fitness(mse = inf) == 0

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

    def plague(self, plague_percent=None):
        if plague_percent is None:
            rand = random.random()
            percent = (self.population_size*rand//2)/self.population_size
        else:
            percent = plague_percent

        print(f"\nOHH NO!!! The black plague came and wiped out about {percent*100:.4}% of the population!")
        for i in range(0, int(self.population_size*percent)):
            rand_index = random.randint(0, self.population_size-1)
            self.population[rand_index] = [random.randint(0, self.gene_max) for j in range(0, self.chromosome_size)]

    def evaluation(self, mse_calculator, expr_gen, satisfactory_mse=10**-6):
        self.mse_list = []
        self.min_mse = np.inf
        self.best_expr = None
        useful_size = None

        for chromosome in self.population:
            expr_gen.reset()
            expr = expr_gen.derivateFromChromosome(chromosome, 5)
            mse = mse_calculator.mean_squared_error(expr)

            # to avoid nan/inf fitness:
            if not np.isfinite(mse):
                mse = np.inf
            elif mse == 0:
                mse = satisfactory_mse

            # finding the best expression:
            if mse < self.min_mse:
                self.min_mse = mse
                self.best_expr = expr
                useful_size = expr_gen.useful_size
            # print(expr, ": ", mse)
            self.mse_list.append(mse)

        print("OK\n\n\tBest expression:\t", self.best_expr)
        print("\tsqrt(MSE):\t\t\t", np.sqrt(self.min_mse), "\t\tUseful size: ", useful_size)

    def evolve(self, filename, crossing_probability=0.8, mutation_rate=0.1, plague_probability=0.1, plague_percent=None,
               selection_exp_const=50, max_generations=200, const_num_digits=3, satisfactory_mse=10**-6):
        # Evaluation:
        print("Generation 1: Evaluating...")
        mse_calculator = DataAnalyzer(filename)
        expr_gen = Expression(const_num_digits)
        self.evaluation(mse_calculator, expr_gen, satisfactory_mse)

        # Evolve loop:
        generation = 1
        while generation < max_generations and min(self.mse_list) > satisfactory_mse:

            # Plague:
            if random.random() < plague_probability:
                self.plague(plague_percent)

            # Selection, crossing and mutation:
            print("\n\nSelecting and crossing ...", end="")
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
            print("OK\nGeneration " + str(generation)+": Evaluating...", end="")

            self.evaluation(mse_calculator, expr_gen, satisfactory_mse)

        # self.best_subject_index = self.mse_list.index(min(self.mse_list))
        # self.best_subject = self.population[self.best_subject_index]

        return generation
