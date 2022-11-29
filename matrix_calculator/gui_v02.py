import tkinter as tk
from sympy.matrices import Matrix
from sympy.parsing.sympy_parser import parse_expr
from sympy.physics.quantum import TensorProduct


#
# Section for GUI
#


class App(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set title of the application window
        root.title('CJ\'s Matrix Calculator')
        # Define functions and create lists for checking, if functions are
        # selected in applicationwindow
        self.singlefunctions = {'Rank': self.calc_rank,
                                'Determinant': self.calc_determinant,
                                'Transpose': self.calc_transpose,
                                'Inverse': self.calc_inverse,
                                'Adjugate': self.calc_adjugate,
                                'CharPolynom': self.calc_charpolynom,
                                'Eigenvalues': self.calc_eigenvalues,
                                'Eigenvectors': self.calc_eigenvectors}
        self.check_singlefunctions = []
        self.vars_singlefunctions = []
        self.linkedfunctions = {'Addition': self.calc_addition,
                                'Subtraction': self.calc_subtraction,
                                'Multiplication': self.calc_multiplication,
                                'Tensor Product': self.calc_tensorproduct,
                                'Linear Equation': self.calc_linearequation}
        self.check_linkedfunctions = []
        self.vars_linkedfunctions = []
        # Function for creating Widgets separated
        self.createWidgets()
        self.pack()

    def createWidgets(self):
        self.frame_matrices = tk.LabelFrame(self, text='Matrices')
        self.frame_matrices.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.label_matrix_1 = tk.Label(self.frame_matrices, text='Matrix 1')
        self.label_matrix_1.grid(row=0, column=0, sticky='W', padx=5)
        self.label_matrix_2 = tk.Label(self.frame_matrices, text='Matrix 2')
        self.label_matrix_2.grid(row=0, column=1, sticky='W', padx=5)
        self.text_matrix_1 = tk.Text(self.frame_matrices, height=10, width=20,
                                     font='timesnewroman 10')
        self.text_matrix_1.focus_set()
        self.text_matrix_1.grid(row=1, column=0, padx=5, pady=5)
        self.text_matrix_2 = tk.Text(self.frame_matrices, height=10, width=20,
                                     font='timesnewroman 10')
        self.text_matrix_2.grid(row=1, column=1, padx=5, pady=5)
        self.frame_selectfunction = tk.LabelFrame(
            self, text='Select functions')
        self.frame_selectfunction.grid(row=1, column=0, columnspan=2,
                                       sticky='EW', padx=5, pady=5)
        self.frame_singlefunction = tk.LabelFrame(self.frame_selectfunction,
                                                  text='Single Matrix Calculations')
        self.frame_singlefunction.grid(
            row=0, column=0, sticky='N', padx=5, pady=5)
        # Creating Checkbuttons from function dictionaries
        for function in self.singlefunctions.keys():
            var_single = tk.BooleanVar()
            var_single.set(False)
            check_single = tk.Checkbutton(self.frame_singlefunction)
            check_single['text'] = function
            check_single['variable'] = var_single
            check_single.pack(anchor='w')
            self.check_singlefunctions.append(check_single)
            self.vars_singlefunctions.append(var_single)
        self.frame_linkedfunction = tk.LabelFrame(self.frame_selectfunction,
                                                  text='Linked Matrices Calculations')
        self.frame_linkedfunction.grid(
            row=0, column=1, sticky='N', padx=5, pady=5)
        # Create Checkbuttons from function dictionaries
        for function in self.linkedfunctions.keys():
            self.var_linked = tk.BooleanVar()
            self.var_linked.set(False)
            self.check_linked = tk.Checkbutton(self.frame_linkedfunction)
            self.check_linked['text'] = function
            self.check_linked['variable'] = self.var_linked
            self.check_linked.pack(anchor='w')
            self.check_linkedfunctions.append(self.check_linked)
            self.vars_linkedfunctions.append(self.var_linked)
        self.button_calc_single_functions = tk.Button(
            self, text='Single Matrix Calc')
        self.button_calc_single_functions.bind('<ButtonPress-1>',
                                               self.calculate_single_functions)
        self.button_calc_single_functions.grid(row=2, column=0, padx=5, pady=5)
        self.button_calc_linked_functions = tk.Button(
            self, text='Linked Matrices Calc')
        self.button_calc_linked_functions.bind('<ButtonPress-1>',
                                               self.calculate_linked_functions)
        self.button_calc_linked_functions.grid(row=2, column=1, padx=5, pady=5)
        self.frame_solution = tk.LabelFrame(self, text='Solution')
        self.frame_solution.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.text_solution = tk.Text(self.frame_solution, height=20, width=40,
                                     font='timesnewroman 10')
        self.text_solution.grid(row=0, column=0, padx=5, pady=5)
        self.text_solution.insert('end', 'Example for a real matrix:\n'
                                         '0 1 0\n'
                                         '1 2 3\n'
                                         '9 1 2\n\n'
                                         'Example for a complex matrix:\n'
                                         '2+2*I 0 1\n'
                                         '2 3-1*I 3\n'
                                         '0 4 3+3*I\n')
        self.scroll_solution = tk.Scrollbar(self.frame_solution)
        self.scroll_solution.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
        self.text_solution['yscrollcommand'] = self.scroll_solution.set
        self.scroll_solution['command'] = self.text_solution.yview

#
# Section of program functions
#

    def calculate_single_functions(self, event):
        """Calculate solution from each selected function in section 'single functions'.
        
        The function first calls convert matrix 1,
        then iterate through selected functions and print the solution.
        """
        self.single_matrix = self.convert_matrix_1()
        self.text_solution.delete('1.0', 'end')
        # Iterate through all functions that are selected (checked by if var.get)
        for i in [name for name, var in zip(self.singlefunctions,
                                            self.vars_singlefunctions) if var.get()]:
            self.text_solution.insert('end', '{} of the matrix:\n'.format(i))
            # Calls every function that is connected in dictionary
            self.singlefunctions[i](self.single_matrix)
            self.text_solution.insert('end', '\n')

    def calculate_linked_functions(self, event):
        """Calculate solutions from each selected function in section 'linked functions'.

        The function first calls convert matrix 1 and convert matrix 2,
        then iterate through selected functions and print the solution.
        """
        self.linked_matrix_1 = self.convert_matrix_1()
        self.linked_matrix_2 = self.convert_matrix_2()
        self.text_solution.delete('1.0', 'end')
        for i in [name for name, var in zip(self.linkedfunctions,
                                            self.vars_linkedfunctions) if var.get()]:
            self.text_solution.insert(
                'end', 'The {} of the matrices:\n'.format(i))
            self.linkedfunctions[i](self.linked_matrix_1, self.linked_matrix_2)
            self.text_solution.insert('end', '\n')

    def convert_matrix_1(self):
        """Convert string input and returns a sympy.Matrix"""
        # Read the text and split it row by row
        self.matrix_1_string = self.text_matrix_1.get(
            '1.0', 'end').strip().split('\n')
        # Using sympy parse_expr to convert splitted string to real or complex number
        self.matrix_1 = Matrix([[parse_expr(j) for j in i.split()]
                               for i in self.matrix_1_string])
        return self.matrix_1

    def convert_matrix_2(self):
        self.matrix_2_string = self.text_matrix_2.get(
            '1.0', 'end').strip().split('\n')
        self.matrix_2 = Matrix([[parse_expr(j) for j in i.split()]
                                for i in self.matrix_2_string])
        return self.matrix_2

    def insert(self, item):
        self.text_solution.insert('end', '{}\n'.format(item))

#
# Section of math functions for calculate single and linked matrices
#

    def calc_rank(self, matrix_1):
        try:
            self.rank_matrix = matrix_1.rank()
            self.insert(self.rank_matrix)
        except Exception as e:
            self.insert(e)

    def calc_determinant(self, matrix_1):
        try:
            self.determinant_matrix = matrix_1.det()
            self.insert(self.determinant_matrix)
        except Exception as e:
            self.insert(e)

    def calc_transpose(self, matrix_1):
        try:
            self.transpose_matrix = matrix_1.T.tolist()
            for row in self.transpose_matrix:
                self.insert(row)
        except Exception as e:
            self.insert(e)

    def calc_inverse(self, matrix_1):
        try:
            self.inverse_matrix = matrix_1.inv().tolist()
            for row in self.inverse_matrix:
                self.insert(row)
        except Exception as e:
            self.insert(e)

    def calc_adjugate(self, matrix_1):
        try:
            self.adjugate_matrix = matrix_1.adjugate().tolist()
            for row in self.adjugate_matrix:
                self.insert(row)
        except Exception as e:
            self.insert(e)

    def calc_charpolynom(self, matrix_1):
        try:
            self.charpolynom_matrix = matrix_1.charpoly().as_expr()
            self.insert(self.charpolynom_matrix)
        except Exception as e:
            self.insert(e)

    def calc_eigenvalues(self, matrix_1):
        try:
            self.eigenvalues_matrix = matrix_1.eigenvals()
            for eigvalue, xtimes in self.eigenvalues_matrix.items():
                self.text_solution.insert('end', 'eigenvalue: {} --> {}x\n'
                                          .format(eigvalue, xtimes))
        except Exception as e:
            self.insert(e)

    def calc_eigenvectors(self, matrix_1):
        try:
            self.eigenvectors_matrix = matrix_1.eigenvects()
            self.eigenvectors_list = []
            for item in self.eigenvectors_matrix:
                for value in item[2]:
                    self.eigenvectors_list.append(value.tolist())
            for i in self.eigenvectors_list:
                self.insert(i)
        except Exception as e:
            self.insert(e)

    def calc_addition(self, matrix_1, matrix_2):
        try:
            self.addition_matrix = matrix_1 + matrix_2
            for row in self.addition_matrix.tolist():
                self.insert(row)
        except Exception as e:
            self.insert(e)

    def calc_subtraction(self, matrix_1, matrix_2):
        try:
            self.subtraction_matrix = matrix_1 - matrix_2
            for row in self.subtraction_matrix.tolist():
                self.insert(row)
        except Exception as e:
            self.insert(e)

    def calc_multiplication(self, matrix_1, matrix_2):
        try:
            self.multiplication_matrix = matrix_1 * matrix_2
            for row in self.multiplication_matrix.tolist():
                self.insert(row)
        except Exception as e:
            self.insert(e)

    def calc_tensorproduct(self, matrix_1, matrix_2):
        try:
            self.tensorproduct_matrix = TensorProduct(matrix_1, matrix_2)
            for row in self.tensorproduct_matrix.tolist():
                self.insert(row)
        except Exception as e:
            self.insert(e)

    def calc_linearequation(self, matrix_1, matrix_2):
        try:
            self.linearequation_matrix = matrix_1.LUsolve(matrix_2)
            for row in self.linearequation_matrix.tolist():
                self.insert(row)
        except Exception as e:
            self.insert(e)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
