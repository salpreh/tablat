# -*- coding: utf-8 -*-
import warnings
import sys
from io import StringIO
from .TabStyle import TabStyle


class Table(object):
    """
    Basic class to print data in a table format.

    Prints a table with a provided headers and data. The number of header titles
        establishes the number of columns in the table.

    Attributes:
        table_data: An iterable containing the data to print in the table.
                    By default an empty list
        headers: Title of each column in the table. By default an empty list.
        style (tablat.TabStyle): Style object to define the aspect of the table.
            If style object is not provided, default style is applied.
            (Default style in `tablat.TabStyle` doc)
    """

    def __init__(self, table_data=[], headers=[], style=None):
        self._table_data = table_data
        self._headers = list(map(str, headers))
        self._num_columns = len(headers)
        self._colspace = 3
        self._column_max = []
        self._align_list = []
        self.style = style

        # Init functions
        self._calc_columns_max_lenght()
        self._alignment_init()
        self._style_check()

    def __getitem__(self, i):
        return self._table_data[i * self._num_columns:i * self._num_columns + self._num_columns]

    def __str__(self):

        # Modify stdout for str buffer
        stdout_backup = sys.stdout
        sys.stdout = StringIO()

        # Generate table (printed to stdout) and restore stdout
        self.print_table()
        table_str = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = stdout_backup

        return table_str

    def __repr__(self):
        print('{\n\t"headers":{},\n\t"data":{},\n\n"columns_lenght":{}\n}'.format(self.headers,
                                                                                  self.table_data,
                                                                                  self._column_max))

    def _calc_columns_max_lenght(self):
        """
        Calculates max lenght of each column based on data in `_table_data` and `_headers`
        """
        if self._num_columns == 0:
            return

        column_max = []
        for head in self._headers:
            column_max.append(len(head))

        for i, data in enumerate(self._table_data):
            if len(str(data)) > column_max[i % self._num_columns]:
                column_max[i % self._num_columns] = len(str(data))

        self._column_max = column_max

    def _update_columns_max_lenght(self, data_list, start_index=0):
        """
        Updates max lenght of columns from a data list.
        """
        if self._num_columns == 0:
            return

        for i, data in enumerate(data_list, start=start_index):
            if len(str(data)) > self._column_max[i % self._num_columns]:
                self._column_max[i % self._num_columns] = len(str(data))

    def _style_check(self):
        if not self.style or not isinstance(self.style, TabStyle):
            self.style = TabStyle()

    def _alignment_init(self):
        """
        Initialize default alingnment based on current number of columns
        """
        align_list = []
        if self._num_columns > 0:
            align_list.append('<')
            for i in range(1, self._num_columns):
                align_list.append('>')

        self._align_list = align_list

    def _adjust_alignment(self):
        """
        Correct alignment list based on `aling_list` lenght and the current number
            of columns
        """
        col_diff = self._num_columns - len(self._align_list)
        if col_diff <= 0:
            self._align_list = self._align_list[:self._num_columns]

        else:
            self._align_list.extend(['>'] * col_diff)

    def _print_hsep(self, char='_', borders=' '):
        """
        Print horizontal separator
        """

        add_lenght = self._colspace * 2
        if self.style.col_sep:
            add_lenght += (self._num_columns -1) * (round(self._colspace / 2) * 2 + 1)
        else:
            add_lenght += (self._num_columns - 1) * self._colspace

        print('{b}{l}{b}'.format(b=borders, l=char*(sum(self._column_max) + add_lenght)))

    def print_table(self):
        """
        Prints a table with the data.
        """

        if not self._num_columns:
            warnings.warn("Unable to calculate the number of columns, you need"
                          "to provide a 'headers' list to generate table layout."
                          "Use headers attribute", UserWarning)
            return

        # Init style vars
        self._style_check()
        col_space = ' ' * self._colspace
        h_borders = ''
        if self.style.col_sep:
            col_space = '{s}{sep}{s}'.format(s=' '*round(self._colspace / 2), sep='|')

        if self.style.borders:
            h_borders = '|'

        # Print separator line
        if self.style.borders:
            self._print_hsep()
        else:
            print()

        # Print headers
        headers_line = '{b}{s}{d:{al}{l}}{sep}'.format(b=h_borders, s=' '*self._colspace, d=self._headers[0],
                                                    al=self._align_list[0], l=self._column_max[0], sep=col_space)

        for (col_lenght, header, align) in zip(self._column_max[1:-1], self._headers[1:-1], self._align_list[1:-1]):
            headers_line += '{d:{al}{l}}{sep}'.format(l=col_lenght, al=align, d=header, sep=col_space)

        headers_line += '{d:{al}{l}}{s}{b}'.format(b=h_borders, s=' '*self._colspace, d=self._headers[-1],
                                                   al=self._align_list[-1], l=self._column_max[-1], sep=col_space)

        print(headers_line)
        self._print_hsep('=' if self.style.row_sep else '-', h_borders)

        # Print lines
        for i, data in enumerate(self._table_data):
            column_index = i % self._num_columns
            if column_index == 0:
                data_line = '{b}{s}{d:{al}{l}}{sep}'.format(b=h_borders, s=' '*self._colspace,
                                                            d=data, al=self._align_list[column_index],
                                                            sep=col_space, l=self._column_max[column_index])

            elif column_index < self._num_columns - 1:
                data_line += '{d:{al}{l}}{sep}'.format(d=data, al=self._align_list[column_index],
                                                       l=self._column_max[column_index], sep=col_space)

            else:
                data_line += '{d:{al}{l}}{s}{b}'.format(d=data, al=self._align_list[column_index],
                                                        l=self._column_max[column_index], s=' '*self._colspace, b=h_borders)
                print(data_line)
                if self.style.row_sep:
                    self._print_hsep('-', h_borders)

        if self.style.borders:
            self._print_hsep(borders='|')

    def add_data(self, data):
        """
        Add more data to the table.

        Args:
            data (list): List of data to add to the `Table`
        """
        current_index = len(self._table_data)
        self._update_columns_max_lenght(data, current_index)
        self._table_data.extend(data)

    @property
    def headers(self):
        """
        Headers of the table. If changed the number of columns will be recalculated.
        """
        return self._headers

    @headers.setter
    def headers(self, new_headers):
        self._headers = new_headers
        self._num_columns = len(new_headers)
        self._calc_columns_max_lenght()
        self._adjust_alignment()

    @property
    def table_data(self):
        """
        Change the data list to in the `Table`.
        """
        return self._table_data

    @table_data.setter
    def table_data(self, tab_data):
        self._table_data
        self._calc_columns_max_lenght()

    @property
    def alignment(self):
        """
        A copy of alignment list of the table. Following string `format` funciton encoding:
            - `<`: Align column data to left.
            - `>`: Align column data to right.
            - `^`: Align column data to center.
        """
        return self._align_list[:]

    @alignment.setter
    def alignment(self, new_align):
        try:
            self._align_list = list(new_align)
            self._adjust_alignment()

        except TypeError:
            print('Align value should be a list (or at least an iterable object)')

    def set_column_align(self, num_column, column_align):
        """
        Set alignment mode for a specific column. Colummn numbering starts form 0.
            Valid values for alignment are:

            - `<`: Align column data to left.
            - `>`: Align column data to right.
            - `^`: Align column data to center.
        """
        valid_values = ['<', '^', '>']
        if column_align not in valid_values:
            raise ValueError('Invalid value. Valid values are {}.\n Chech method doc for more info'.format(valid_values))

        try:
            self._align_list[num_column] = column_align

        except IndexError:
            raise IndexError('Invalid column index. Current number of columns: {}, index input: {}'.format(self._num_columns, num_column))
