# -*- coding: utf-8 -*-
import importlib.util
import sys
from pathlib import Path

# Global vars
test_path = Path("../")

if __name__ == "__main__":

    # Import file under test
    spec = importlib.util.spec_from_file_location("tablat", "../tablat/Table.py")
    target = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(target)
    Table = target.Table

    header = ['FILE_NAME', 'FOLDER', 'FILES_IN']
    data = []
    for file_path in test_path.iterdir():
        data.append(file_path.name)
        if file_path.is_dir():
            data.extend(['YES', len([f for f in file_path.iterdir()])])

        else:
            data.extend(['NO', 0])

    my_table = Table(data, header)
    my_table.print_table()

    # getitem test
    print(f'\n1st Row: {my_table[0]}')
    print(f'2nd row, 1st column: {my_table[1][0]}')
