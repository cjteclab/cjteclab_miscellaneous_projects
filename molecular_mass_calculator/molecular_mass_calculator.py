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
    """Representation of a searched Molecule.

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

    Examples
    --------
    >>> test_molecule_a = Molecule()
    Please enter molecular formular of the molecule: H20
    >>> test_molecule_a.molecule_formular
    'H2O'
    >>> test_molecule_a.molecule_elements
    {'H': '2', 'O': '1'}
    >>> test_molecule_a.molecule_mass
    18.01528

    >>> test_molecule_b = Molecule()
    Please enter molecular formular of the molecule: H2SO4
    >>> test_molecule_b.molecule_formular
    'H2SO4'
    >>> test_molecule_b.molecule_elements
    {'H': '2', 'S': 1, 'O': '4'}
    >>> test_molecule_b.molecule_mass
    98.07848
    """

    def __init__(self):
        """Initiate instances of class Molecule()."""
        self.molecule_formular = self.get_molecule_formular()
        self.molecule_elements = self.extract_elements(self.molecule_formular)
        self.molecule_mass = self.calc_molecule_weight(self.molecule_elements)

    def get_molecule_formular(self) -> str:
        """Ask user for molecule formular.

        Returns
        -------
        str
            Representation of the searched molecular formular.
        """
        return input('Please enter molecular formular of the molecule: ')

    def extract_elements(self, molecule_formular: str) -> Dict:
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
        """
        # Can be pack into a dictcomprehension, but less readability
        molecule_elements = {}
        # Split the string at each upper letter
        split_string = re.sub(r"([A-Z])", r" \1", molecule_formular).strip().split()
        for unit in split_string:
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
    history = []
    while True:
        clear_output()
        history.append(Molecule())
        if history[-1].molecule_mass == 0:
            print("The molecular formular can't be calculated.")
            del history[-1]
        else:
            print(f'The molecule mass of {history[-1].molecule_formular} is: '
                  f'{history[-1].molecule_mass} g/mol')
        print()
        decision = input('Calculate another moleule mass (y/n) '
                         'or look at history (h)? ')
        if decision == 'n':
            break
        elif decision == 'h':
            clear_output()
            print('History:')
            print()
            for molecule in history:
                print(f'{molecule.molecule_formular} = '
                      f'{molecule.molecule_mass} g/mol')
            print()
            if input('Calculate another molecule mass (y/n): ') == 'n':
                break
    print()
    print('Have a nice day!')


if __name__ == '__main__':
    main()
