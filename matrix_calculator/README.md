# CJ's Matrix Calculator

This project was my final project for CS50.

#### Video Demo: https://youtu.be/q6e-d5AgfQg

## Welcome | اهلا وسهلا | স্বাগত| 欢迎 | Willkommen | Bienvenue | स्वागत है | ようこそ | Bem-vindo | Ми́лости про́сим | Bienvenida

CS50 world,

my name is CJ and I am a chemical engineer from Germany. With my background and experience in chemical quantum mechanics, my main interests are all combinations of Chemistry, Computational Chemistry, Data Science and Quantum Computing and their applications (in particular molecular modeling/simulation/analytics).

For my CS50 final project, I developed a small GUI application “**CJ’s Matrix Calculator**'' for matrix calculations which can be used by people with no programming background. The application calculates different single matrix properties and linked matrix operations using the python library sympy. The application uses Tkinter as a graphical user interface, a python GUI framework that is part of the Python standard library.

Currently, the application contains the following single matrix properties: Rank, Determinant, Transpose, Inverse, Adjugate, Characteristic Polynom, Eigenvalues and Eigenvectors. And the following linked matrix operations: Addition, Subtraction, Multiplication, Tensor Product and Linear Equation.

### The intention of the project
Quantum Mechanics is a big part of my interests. To understand quantum mechanics a basic understanding of linear algebra is crucial. As I learned the mathematical basics of quantum mechanics, there are many exercises to determine various single matrix properties like adjugate, inverse or eigenvalues and eigenvectors. To check my results or simplify my calculations I need a program that supports my calculations. Maybe someone else can use it for similar tasks.

### Workflow
The graphical user interface of the application is split into three sections.

In the *upper section*, you can input one (for single matrix calculations) or two (for linked matrix calculations) real or complex (e.g. 3+3*I) matrices.

In the *middle section,* you can select the properties (single matrix calculations) or the operations (linked matrix calculations) you wish to apply. After selecting the functions you want to apply, you have to click “Single Matrix Calc” (if you want single matrix properties) or “Linked Matrices Calc” (if you want linked matrix operations).

In the *lower section,* you get the results of the calculations.

### Design Choices
**GUI vs. CommandLine**: Because of the usage for people with no programming background I decided to use a user interface instead of a command line for interaction. Additionally, the user interface is easier to use for fast and simple matrix calculations.

**GUI Framework**: Python has a lot of different GUI frameworks. I decided to use Tkinter because Tkinter is the only framework that’s built into the Python standard library and it is cross-platform so the same code works on Windows, macOS, and Linux. Further, I personally prefer lightweight and simple frameworks.

**Library for calculations**: There are different python libraries to calculate single matrix properties and linked matrices operations. For example numpy, scipy or sympy. After several tries, I decided to use sympy, because the function's outputs are prettier to print in the Tkinter text field.

### Issues
Handle difficulties in the outcome of eigenvectors.
Add new properties and operations.
Save and export the calculation (matrices input and solution output).

**My Name is CJ, and this is CS50.**


