import numpy as np

class Grammar:

    var = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8']
    func = ['np.sin', 'np.cos', 'np.tan', 'np.log', 'np.exp']
    operations = ['+', '-', '*', '/']
    initial = ['<exp>']

    derivations = [['<exp>', '<op>', '<exp>'],
                   ['(', '<exp>', '<op>', '<exp>', ')'],
                   ['<var>'],
                   ['<func>', '(', '<exp>', ')'],
                   ['<const>'],
                   ['<var>', '**', '<dig>']
                   ]
    bits = ['0', '1']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    const_derivations = ['<bit>']

    working_on = 0

    def __index__(self, num_digits):
        self.num_digits = num_digits
        self.num_derivations = len(self.derivations)
        self.num_operations = len(self.operations)
        self.num_var = len(self.var)
        self.num_func = len(self.func)

        for i in range(1, num_digits):
            self.const_derivations.append('<dig>')

    def derivateExpression(self, cromossome):

        if self.initial[self.working_on] == '<exp>':
            new_expression = cromossome % self.num_derivations
            to_remove = self.initial[self.working_on]
            #self.initial[self.working_on] = self.derivations[new_expression]
            length = len(self.derivations[new_expression])

            for i in range(0, length):
                if i == 0:
                    self.initial.insert(self.working_on, self.derivations[new_expression][i])
                    self.initial.remove(to_remove)
                else:
                    self.initial.insert(self.working_on + 1, self.derivations[new_expression][i])


        elif self.initial[self.working_on] == '<op>':
            new_op = cromossome % self.num_operations
            self.initial[self.working_on] = self.operations[new_op]

        elif self.initial[self.working_on] == '<var>':
            new_var = cromossome % self.num_var
            self.initial[self.working_on] = self.var[new_var]

        elif self.initial[self.working_on] == '<func>':
            new_func = cromossome % self.num_func
            self.initial[self.working_on] = self.func[new_func]

        elif self.initial[self.working_on] == '<const>':
            
