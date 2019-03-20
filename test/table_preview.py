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
load_file_test = Path("./input/load_test.json")


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


def create_tab_columns():
    """
    Create table from a `dict` feeding data as columns
    """
    column_data = {
        'FILE_NAME': [],
        'FOLDER': [],
        'FILES_IN': []
    }
    for file_path in test_path.iterdir():
        column_data['FILE_NAME'].append(file_path.name)
        column_data['FOLDER'].append('Y' if file_path.is_dir() else 'N')
        column_data['FILES_IN'].append(len([f for f in file_path.iterdir()]) if file_path.is_dir() else 0)

    Table().set_column_content(column_data).print_table()


def print_all_style_tabs(table):
    """
    Prints all style variants of `Table` object
    """
    bool_opt = [True, False]
    print('>> Printing style table combinations...')
    for (borders, col_sep, row_sep) in set(itertools.combinations(bool_opt * 3, 3)):
        my_table.style.update(borders, col_sep, row_sep)
        print_table_debug(
            f'> borders={borders} / col_separator={col_sep} / row_separator={row_sep}\n',
            table
        )


def print_align_test(table):

    # Change alignment list
    table.alignment = ['^', '<', '>']
    print_table_debug(f'Alignment changed to: {table.alignment}\n', table)

    # Update specific columns
    table.set_column_align(1, '^')
    table.set_column_align(0, '<')
    print_table_debug(
        f"Alignment changed. Column 1 -> '{table.alignment[0]}' / Column 2 -> '{table.alignment[1]}'",
        table
    )


def print_filter_test(table):
    # Hide columns
    print(f'Hide column 2\n')
    table.print_table(hide_columns=[1])
    print('-'*60)

    # Show columns
    print(f'Show columns 1 an 2\n')
    table.print_table(show_columns=[0, 1])
    print('-'*60)

    # Show and hide
    print(f'Show column 1, hide 1 and 3\n')
    table.print_table(show_columns=[0], hide_columns=[0, 2])
    print('-'*60)


def print_loaded_test():
    table = Table()
    table.load_data(load_file_test)
    table.print_table()


def print_table_debug(title, table):
    print(title+'\n')
    table.print_table()
    print('-'*60)


if __name__ == "__main__":
    my_table = create_test_tab()
    print_all_style_tabs(my_table)
    print_align_test(my_table)
    print_filter_test(my_table)
    create_tab_columns()
    print_loaded_test()

    # getitem test
    print(f'\n1st Row: {my_table[0]}')
    print(f'2nd row, 1st column: {my_table[1][0]}')
