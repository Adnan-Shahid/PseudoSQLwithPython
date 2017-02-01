class Table():
    '''A class to represent a SQuEaL table'''

    def table_data(self, column_titles, columns):
        '''(Table, list, list) -> NoneType
        takes in the keys and columns from read_table and
        links them together via key: data using dictionaries
        Compiles all data into a dictionary
        REQ: len(keys) > 0
        REQ: len(columns) > 0
        '''
        # getting all the keys of the dictionary for future use
        self._column_titles = column_titles

        # getting the data for the keys for future use
        self._columns = columns

        # creating the dictionary so that it can be moved
        self._all_data = {}

        # get the amount of rows within a table
        self._rows = len(columns[0])

        # maps columns to their respective column titles
        # data containing years will go into the year column title
        for i in range(len(column_titles)):
            self._all_data[column_titles[i]] = columns[i]

    def num_rows(self):
        '''(Table) -> int
        returns the number of rows within a given Table
        '''
        return self._rows

    def get_keys(self):
        '''(Table) -> list
        returns the keys the dictionary within the object
        '''
        return self._column_titles

    def get_columns(self):
        '''(Table) -> list
        returns the data for the keys of the dictionary within the object
        '''
        return self._columns

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType
        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
        column_name: list_of_values
        REQ: the dictionary is properly formatted
        '''
        self._all_data = new_dict
        # getting the list of keys
        list_keys = list(self._all_data.keys())
        # updating the value for the number of rows in the Table
        self._rows = len(self._all_data[list_keys[0]])

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self._all_data


class Database():
    '''A class to represent a SQuEaL database'''
    def database_data(self, title_list, table_list):
        '''(Database, list, list) -> NoneType
        takes in the titles and tables from read_database and
        links them together via title_list: table_list using dictionaries
        Compiles all data into a dictionary
        REQ: len(title_list) > 0
        REQ: len(table_list) > 0
        '''
        # creating the dictionary so that it can be moved
        self._all_tables = {}

        # maps columns to their respective column titles
        # data containing years will go into the year column title
        for i in range(len(title_list)):
            self._all_tables[title_list[i]] = table_list[i]

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
        table_name: table
        REQ: the dictionary is properly formatted
        '''
        self._all_tables = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._all_tables
