class Grammar:
    var = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
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

    def __init__(self):
        self.num_derivations = len(self.derivations)
        self.num_operations = len(self.operations)
        self.num_var = len(self.var)
        self.num_func = len(self.func)
        self.const_derivations = ['<bit>', '.']