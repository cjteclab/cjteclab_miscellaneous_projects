#!/usr/bin/env python3
""" Molecular Mass Calculator by cjteclab

Calculate the molecular mass of a molecule formular.

Usage
-----
When you are prompted to enter a molecular formular, you can enter any
molecular formuar(for example: H2O, H2SO4, TiO2, H2, NaCl).
After the result is displayed you can choose between three options:
    1. Calculate a new molecule mass of a molecule.
    2. Show history of calculated molecules.
    3. Exit Molecular Mass Calculator.

Author
------
cjteclab
"""
import os
import json
import re
from typing import Dict


class Molecule():
    """ Representation of a searched Molecule.

    Parameters
    ----------
    molecule_string : str
        Representation of the searched molecular formular.

    Attributes
    ----------
    molecule_string : str
        Representation of the searched molecular formular.
    molecule_elements : dict of {str : str}
        Items consist of element symbol and the frequency of the element.
    molecule_mass : float
        Weight of the molecule with the unit g/mol.

    Methods
    -------
    extract_elements(molecule_string):
        Extracting elements symbol and frequency out of molecular formular.
    calc_molecule_weight(molecule_elements):
        Caclulate the weight of the molecule.

    """

    def __init__(self, molecule_string: str):
        self.molecule_string = molecule_string
        self.molecule_elements = self.extract_elements(self.molecule_string)
        self.molecule_mass = self.calc_molecule_weight(self.molecule_elements)

    def extract_elements(self, molecule_string: str) -> Dict:
        """Extracting elements symbol and frequency out of molecular formular.

        Parameters
        ----------
        molecule_string : str
            Representation of the molecular formular the user want
            to calculate.

        Returns
        -------
        dict of {str : str}
            Items consist of element symbol and the frequency of the element.

        Examples
        --------
        >>> a = 'H2O'
        >>> test_mol_a = Molecule(a)
        >>> test_mol_a.extract_elements(a)
        {'H': '2', 'O': '1'}

        >>> b = 'H2SO4'
        >>> test_mol_b = Molecule(b)
        >>> test_mol_b.extract_elements(b)
        {'H': '2', 'S': 1, 'O': '4'}
        """
        # Can be pack into a dictcomprehension, but less readability
        molecule_elements = {}
        # Split the string at each upper letter
        splitted_string = re.sub(r"([A-Z])", r" \1", molecule_string).strip().split()
        for unit in splitted_string:
            if unit.isalpha():
                molecule_elements.update({unit: '1'})
            else:
                # Split the string between letter and number
                # add dict(element: count) via .update to molecule_dict
                # dict() expects an iterable of two-item iterables, so re.split
                # need to put in a list
                molecule_elements.update(dict([re.split('(?<=\D)(?=\d)', unit)]))
        return molecule_elements

    def calc_molecule_weight(self, molecule_elements: Dict) -> float:
        """Caclulate the weight of the molecule.

        Parameters
        ----------
        molecule_elements : dict of {str : str}
            Items consist of element symbol and the frequency of the element.

        Returns
        -------
        float
            Weight of the molecule with the unit g/mol.
        --------
        >>> a = 'H2O'
        >>> a_dict = {'H': '2', 'O': '1'}
        >>> test_mol_a = Molecule(a)
        >>> test_mol_a.calc_molecule_weight(a)
        18.01528

        >>> b = 'H2O'
        >>> b_dict = {'H': '2', 'S': 1 'O': '4'}
        >>> test_mol_b = Molecule(b)
        >>> test_mol_b.calc_molecule_weight(b)
        98.07848
        """
        molecule_mass = 0
        try:
            for element, count in molecule_elements.items():
                molecule_mass += PERIODICTABLE[element] * int(count)
                # Pythonic Way:
                # sum(TABLEOFELEMENTS[element] * int(count) for element, count
                # in molecule_elements.items())
            return molecule_mass
        except KeyError:
            return 0


def clear_output():
    """Clear Python shell"""
    os.system('cls' if os.name == 'nt' else 'clear')


def read_periodictable() -> Dict:
    """Read json file that contains Periodic Table.

    Returns
    -------
    dict of {str : float}
        Items consist of element symbol and the mass of the element.

    Examples
    --------
    >>> a = read_periodictable()
    >>> print(a['H'])
    1.00794

    >>> b = read_periodictable()
    >>> print(b['H'] + b['H'] + b['O'])
    18.01528
    """
    with open('periodictable.json') as file:
        periodictable = json.load(file)
    return periodictable


PERIODICTABLE = read_periodictable()
""" A periodic table as dict of {str : float}"""


def main():
    looping = True
    history = []
    while looping:
        clear_output()
        input_molecule = input('Please enter molecular formular of the molecule: ')
        history.append(Molecule(input_molecule))
        if history[-1].molecule_mass == 0:
            print("The molecular formular you have enterd can't be calculated.")
        else:
            print(f'The molecule mass of {history[-1].molecule_string} is: '
                  f'{history[-1].molecule_mass} g/mol')
        print()
        decision = input('Calculate another moleule mass (y/n) '
                         'or look at history (h)? ')
        print()
        if decision == 'n':
            looping = False
            print('Have a nice day!')
        elif decision == 'h':
            clear_output()
            print('History:')
            print()
            for molecule in history:
                print(f'{molecule.molecule_string} = {molecule.molecule_mass} g/mol')
            print()
            if input('Calculate another molecule mass (y/n): ') == 'n':
                looping = False
                print()
                print('Have a nice day!')


if __name__ == '__main__':
    main()
