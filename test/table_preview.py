# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
from tablat import Table, TabStyle
import importlib.util
import itertools
from pathlib import Path

# Global vars
test_path = Path("../")


def create_test_tab():
    """
    Creates a basic table for test purposes
    """
    header = ['FILE_NAME', 'FOLDER', 'FILES_IN']
    my_table = Table(headers=header)
    for file_path in test_path.iterdir():
        my_table.add_data([file_path.name])
        if file_path.is_dir():
            my_table.add_data(['Y', len([f for f in file_path.iterdir()])])

        else:
            my_table.add_data(['N', 0])

    return my_table


def print_all_style_tabs(table):
    """
    Prints all style variants of `Table` object
    """
    bool_opt = [True, False]
    print('>> Printing style table combinations...')
    for (borders, col_sep, row_sep) in set(itertools.combinations(bool_opt * 3, 3)):
        print(f'> borders={borders} / col_separator={col_sep} / row_separator={row_sep}\n')
        my_table.style.update(borders, col_sep, row_sep)
        my_table.set_column_align(1, '^')
        my_table.print_table()
        print('-'*60)


if __name__ == "__main__":
    my_table = create_test_tab()
    print_all_style_tabs(my_table)

    # getitem test
    print(f'\n1st Row: {my_table[0]}')
    print(f'2nd row, 1st column: {my_table[1][0]}')
