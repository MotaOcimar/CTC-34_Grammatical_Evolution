from Grammar.EnumClasses import State
from Grammar.Grammar import Grammar


class Expression(Grammar):

    working_on = 0
    state = None
    useful_size = 0

    def __init__(self, num_digits=15):
        Grammar.__init__(self)
        self.num_digits = num_digits

        for i in range(1, num_digits):
            self.const_derivations.append('<dig>')

    def derivateExpression(self, gene):

        if self.working_on < len(self.initial):

            if self.initial[self.working_on] == '<exp>':
                new_expression = gene % self.num_derivations
                to_remove = self.initial[self.working_on]
                #self.initial[self.working_on] = self.derivations[new_expression]
                length = len(self.derivations[new_expression])

                for i in range(0, length):
                    if i == 0:
                        self.initial.insert(self.working_on, self.derivations[new_expression][i])
                        self.initial.remove(to_remove)
                    else:
                        self.initial.insert(self.working_on + i, self.derivations[new_expression][i])

            elif self.initial[self.working_on] == '<op>':
                new_op = gene % self.num_operations
                self.initial[self.working_on] = self.operations[new_op]

            elif self.initial[self.working_on] == '<var>':
                new_var = gene % self.num_var
                self.initial[self.working_on] = self.var[new_var]

            elif self.initial[self.working_on] == '<func>':
                new_func = gene % self.num_func
                self.initial[self.working_on] = self.func[new_func]

            elif self.initial[self.working_on] == '<const>':
                length = len(self.const_derivations)
                to_remove = self.initial[self.working_on]

                for i in range(0, length):
                    if i == 0:
                        self.initial.insert(self.working_on, self.const_derivations[0])
                        self.initial.remove(to_remove)
                    else:
                        self.initial.insert(self.working_on + i, self.const_derivations[i])

                new_bit = str(gene % 2)

                self.initial[self.working_on] = new_bit

            elif self.initial[self.working_on] == '<bit>':
                self.initial[self.working_on] = str(gene % 2)

            elif self.initial[self.working_on] == '<dig>':
                self.initial[self.working_on] = str(gene % 10)

            else:
                self.working_on += 1
                return self.derivateExpression(gene)

            return State.not_finished

        else:
            return State.finished

    def derivateFromChromosome(self, chromosome, maximum=3):

        self.useful_size = 0
        for i in range(0, maximum):
            for gene in chromosome:
                self.useful_size += 1
                self.state = self.derivateExpression(gene)
                if self.state == State.finished:
                    break

            if self.state == State.finished:
                return "".join(self.initial)

        return "np.nan"

    def reset(self):
        self.state = None
        self.working_on = 0
        Grammar.initial = ['<exp>']
        self.__init__(self.num_digits)
