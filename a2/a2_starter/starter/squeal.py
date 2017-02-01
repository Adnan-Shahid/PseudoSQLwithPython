from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


# creating globals
WHERE_TOKEN = 4
FILES_IN_QUERY = 3
WHERE_VALUE = 5
COLUMN_SELECT = 1
COLUMN_EQUAL_VALUE = 0
COLUMN_EQUAL_COLUMN = 1
COLUMN_GREATER_VALUE = 2
COLUMN_GREATER_COLUMN = 3


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = table.num_rows()

    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))


def cartesian_product(table1, table2):
    '''cartesian_product: (Table, Table) -> Table
    creates a new table where each row in the first table is paired
    with every row in the second table.
    REQ: both tables are properly formatted
    REQ: the tables aren't empty

    >>> x = Table()
    >>> y = Table()
    >>> x.table_data(['title','year'],[['m1','m2'],['5','6']])
    >>> y.table_data(['t','y','money'],[['m1','m2','m3'],
    ['5','6','7'],['1.0','2.0','3.0']])
    >>> z = cartesian_product(x,y)
    >>> z.get_dict()
    {'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
    'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
    'year': ['5', '5', '5', '6', '6', '6'],
    'y': ['5', '6', '7', '5', '6', '7'],
    'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']}

    >>> x = Table()
    >>> y = Table()
    >>> x.table_data(['title'],[['m1'],['5']])
    >>> y.table_data['t','y'],[['m1','m2'],['5','6']])
    >>> z = cartesian_product(x,y)
    >>> z.get_dict()
    {'t': ['m1', 'm2'], 'y': ['5', '6'], 'title': ['m1', 'm1']}
    '''
    new_dict = {}
    # getting the dictionaries for both tables
    table1_dict = table1._all_data
    table2_dict = table2._all_data
    # finding the length of the values of the dictionary
    table1_dict_length = len(list(table1_dict.values())[0])
    table2_dict_length = len(list(table2_dict.values())[0])

    # concatenates both dictionaries
    # checks for all keys in table1_dict
    for key in table1_dict:
        # for all the values in the list of said key
        for value in table1_dict[key]:
            # if the key isn't in the dictionary
            if key not in new_dict:
                # empties the value
                new_dict[key] = []
                # adds every element in the list of values to the dict
                new_dict[key].extend([value]*table2_dict_length)
            else:
                # adds every element in the list of values to the dict
                new_dict[key].extend([value]*table2_dict_length)
    # adds every value in table2_dict to the dictionary
    for key in table2_dict:
        # repeats for every element that should be repeated
        new_dict[key] = table2_dict[key]*table1_dict_length

    # gets the keys of the new dictionary
    list_of_keys = list(new_dict.keys())
    # holds the data for each key of the new dictionary
    list_values = []
    # storing the values per key
    for i in range(len(list_of_keys)):
        value = new_dict[list_of_keys[i]]
        list_values.append(value)

    # making the new table
    new_table = Table()
    # inputting all data into the new table
    new_table.table_data(list_of_keys, list_values)

    return new_table


def which_where_query(where_clause, list_tables):
    '''(string, list of Tables) -> list
    Checks which clause is being done for the where token
    All possibilities are
    column_name1=column_name2, column_name1>column_name2,
    column_name1='value', or column_name1>'value'
    It will return a list containing the two items being compared
    and the clause operator of > or =

    REQ: where_clause is of one of the formats:
    column_name1=column_name2, column_name1>column_name2,
    column_name1='value', or column_name1>'value'

    REQ: len(list_tables) > 1

    >>> x = Table()
    >>> y = Table()
    >>> x.table_data(['title','year'],[['m1','m2'],['5','6']])
    >>> y.table_data(['t','y','money'],[['m1','m2','m3'],
                     ['5','6','7'],['1.0','2.0','3.0']])
    >>> tables = []
    >>> tables.append(x)
    >>> tables.append(y)
    >>> which_where_query('y>year',tables) == 3
    True

    >>> which_where_query('y=year',tables) == COLUMN_EQUAL_COLUMN
    True

    >>> which_where_query('y=6',tables) == COLUMN_EQUAL_VALUE
    True

    >>> which_where_query('y>6',tables) == COLUMN_GREATER_VALUE
    True
    '''
    # this is the variable that will determine the comparison type
    compare_type = 99
    # if compare_type = 0, it is a column_name1='value' comparison
    # if compare_type = 1, it is a column_name1=column_name2 comparison
    # if compare_type = 2, it is a column_name1>'value' comparison
    # if compare_type = 3, it is a column_name1>column_name2 comparison

    # list of keys for all dictionaries
    list_keys = []

    # creating the list of keys compiled for all tables in the query
    for i in range(len(list_tables)):
        # gets the dictionary per file/table
        table_dict = list_tables[i]._all_data
        # gets the keys for the dictionary
        table_keys = list(table_dict.keys())
        # adds the list of keys to the compiled list of keys
        # element by element
        list_keys.extend(table_keys)

    if '=' in where_clause:
        # Indicates whether it is a comparison of
        # columns or of a column and a 'value'

        # gets the list containing both things required for comparison
        where_list = where_clause.split('=')

        # determining which equal clause it is
        if where_list[1] in list_keys:
            # it is a column_name1=column_name2 comparison
            column_type = COLUMN_EQUAL_COLUMN
        else:
            # it is a column_name1='value' comparison
            column_type = COLUMN_EQUAL_VALUE

    elif '>' in where_clause:
        # Indicates whether it is a comparison of
        # columns or of a column and a 'value'

        # gets the list of the things being compared
        where_list = where_clause.split('>')

        # determining which > clause it is
        if where_list[1] in list_keys:
            # it is a column_name1>column_name2 comparison
            column_type = COLUMN_GREATER_COLUMN
        else:
            # it is a column_name1>'value'
            column_type = COLUMN_GREATER_VALUE

    return column_type


def select_token(query_list, files, new_table):
    '''(list, list, Table) -> Table
    does the select token from sQuEaL, creates a new table based on the
    requested columns
    REQ: query_list contains at least 4 items
    REQ: files is of proper format
    REQ: table is not empty
    '''
    if (query_list[COLUMN_SELECT] != '*'):
        # gets the list of columns that are asked for
        # stores them as essentially keys from calling their data
        columns = query_list[COLUMN_SELECT].split(',')

        # gets the dictionary for the required table
        new_table_dict = new_table._all_data

        # holds the data for each key of the new dictionary
        list_values = []

        # storing the values per key asked for in a list
        for i in range(len(columns)):
            value = new_table_dict[columns[i]]
            list_values.append(value)

        # creates a new Table with the required columns
        new_table = Table()
        # fills the table with data
        new_table.table_data(columns, list_values)

    return new_table


def equal_value(new_table, where_query):
    '''(Table, string) -> NoneType
    Does the where token for when column='value'
    Compares when the requested column = the correct value
    and deletes any values within the table that do not have the
    the requested value

    REQ: where_query is of the form column=value
    REQ: the column is within the table
    REQ: the table contains values

    >>> x = Table()
    >>> x.set_dict({'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
        'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
    'year': ['5', '5', '5', '6', '6', '6'],
    'y': ['5', '6', '7', '5', '6', '7'],
    'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']})
    >>> equal_value(x, t=m1)
    >>> x._all_data == {'t': ['m1', 'm1'], 'y': ['5', '5'],
        'year': ['5', '6'], 'title': ['m1', 'm2'],
        'money': ['1.0', '1.0']}
    True

    >>> x = Table()
    >>> x.set_dict({'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
        'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
    'year': ['5', '5', '5', '6', '6', '6'],
    'y': ['5', '6', '7', '5', '6', '7'],
    'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']})
    >>> equal_value(x, year=5)
    >>> x._all_data == {'year': ['5', '5', '5'],
        't': ['m1', 'm2', 'm3'], 'money': ['1.0', '2.0', '3.0'],
        'y': ['5', '6', '7'], 'title': ['m1', 'm1', 'm1']}
    True
    '''
    # getting the list of keys
    list_keys = list(new_table._all_data.keys())

    rows = new_table.num_rows()
    # getting a list of the columns that'll be compared

    list_comparison = where_query.split('=')
    first_column = list_comparison[0]
    value = list_comparison[1]

    # this is a list of indexes that will contain any index
    # that should be deleted based on the where constraint
    index_deletion = []

    # tables dictionary is new_table._all_data
    for i in range(rows):
        # checks if the first column value is <= the second column value
        # checks the ith term
        if (new_table._all_data[first_column][i] != value):
            # adds to a list of ind
            index_deletion.append(i)

    # reverses the index of deletion so it will work with .pop()
    # and removes last value
    index_deletion.reverse()

    # check every column and delete the row required from the column
    for i in index_deletion:
        for keys in new_table._all_data:
            useless_value = new_table._all_data[keys].pop(i)

    # getting the list of the new keys to update the row variable
    list_keys = list(new_table._all_data.keys())
    new_table._rows = len(new_table._all_data[list_keys[0]])


def equal_column(new_table, where_query):
    '''(Table, string) -> NoneType
    Does the where token for when column=column2
    Compares when the requested column = the correct value
    and deletes any values within the table that do not have the
    the requested value

    REQ: where_query is of the form column=column2
    REQ: the columns are within the table
    REQ: the table contains values

    >>> x = Table()
    >>> x.set_dict({'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
        'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
        'year': ['5', '5', '5', '6', '6', '6'],
        'y': ['5', '6', '7', '5', '6', '7'],
        'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']})
    >>> equal_column(x,'y=year')
    >>> x._all_data == {'title': ['m1', 'm2'], 'year': ['5', '6'],
                       'y': ['5', '6'], 't': ['m1', 'm2'],
                       'money': ['1.0', '2.0']}
    True

    >>> x = Table()
    >>> x.set_dict({'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
        'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
        'year': ['5', '5', '5', '6', '6', '6'],
        'y': ['5', '6', '7', '5', '6', '7'],
        'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']})
    >>> equal_column(x, 't=title')
    >>> x == {'money': ['1.0', '2.0'], 't': ['m1', 'm2'],
             'title': ['m1', 'm2'], 'year': ['5', '6'],
             'y': ['5', '6']}
    True
    '''
    # getting the list of keys
    list_keys = list(new_table._all_data.keys())

    rows = new_table.num_rows()
    # getting a list of the columns that'll be compared
    list_comparison = where_query.split('=')
    first_column = list_comparison[0]
    second_column = list_comparison[1]

    # this is a list of indexes that will contain any index
    # that should be deleted based on the where constraint
    index_deletion = []

    # tables dictionary is new_table._all_data
    for i in range(rows):
        # checks if the first column value is = the second column value
        # checks the ith term
        if (new_table._all_data[first_column][i] != (new_table._all_data
                                                     [second_column][i])):
            index_deletion.append(i)

    # reverses the index of deletion so it will work with .pop()
    # and removes last value
    index_deletion.reverse()

    # check every column and delete the row required from the column
    for i in index_deletion:
        for keys in new_table._all_data:
            useless_value = new_table._all_data[keys].pop(i)

    # getting the list of the new keys to update the row variable
    list_keys = list(new_table._all_data.keys())
    new_table._rows = len(new_table._all_data[list_keys[0]])


def greater_value(new_table, where_query):
    '''(Table, string) -> NoneType
    Does the where token for when column>value
    Compares when the requested column > the correct value
    and deletes any values within the table that aren't greater
    than the requested value

    REQ: where_query is of the form column>value
    REQ: the column is within the table
    REQ: the table contains values

    >>> x = Table()
    >>> x.set_dict({'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
        'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
        'year': ['5', '5', '5', '6', '6', '6'],
        'y': ['5', '6', '7', '5', '6', '7'],
        'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']})
    >>> greater_value(x, 'y>6')
    >>> x._all_data == {'t': ['m3', 'm3'], 'year': ['5', '6'],
                       'money': ['3.0', '3.0'], 'title': ['m1', 'm2'],
                       'y': ['7', '7']}
    True

    >>> x = Table()
    >>> x.set_dict({'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
        'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
        'year': ['5', '5', '5', '6', '6', '6'],
        'y': ['5', '6', '7', '5', '6', '7'],
        'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']})
    >>> greater_value(x, 'y>banana')
    >>> x._all_data == {'year': [], 'money': [], 'title': [],
                       't': [], 'y': []}
    True
    '''
    # getting the list of keys
    list_keys = list(new_table._all_data.keys())

    rows = new_table.num_rows()
    # getting a list of the columns that'll be compared
    list_comparison = where_query.split('>')
    first_column = list_comparison[0]
    value = list_comparison[1]

    # this is a list of indexes that will contain any index
    # that should be deleted based on the where constraint
    index_deletion = []

    # tables dictionary is new_table._all_data
    for i in range(rows):
        # checks if the first column value is <= the given value
        # checks the ith term
        if (new_table._all_data[first_column][i] <= value):
            index_deletion.append(i)

    # reverses the index of deletion so it will work with .pop()
    # and removes last value
    index_deletion.reverse()

    # check every column and delete the row required from the column
    for i in index_deletion:
        for keys in new_table._all_data:
            useless_value = new_table._all_data[keys].pop(i)

    # getting the list of the new keys to update the row variable
    list_keys = list(new_table._all_data.keys())
    new_table._rows = len(new_table._all_data[list_keys[0]])


def greater_column(new_table, where_query):
    '''(Table, string) -> NoneType
    Does the where token for when column>column
    Compares when the requested column > columns
    and deletes any values within the table that aren't greater
    than the requested column

    REQ: where_query is of the form column>column2
    REQ: the columns are within the table
    REQ: the table contains values

    >>> x = Table()
    >>> x.set_dict({'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
        'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
        'year': ['5', '5', '5', '6', '6', '6'],
        'y': ['5', '6', '7', '5', '6', '7'],
        'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']})
    >>> greater_column(x, 'y>year')
    >>> x._all_data == {'year': ['5', '5', '6'], 'title': ['m1', 'm1', 'm2'],
                       't': ['m2', 'm3', 'm3'],
                       'money': ['2.0', '3.0', '3.0'], 'y': ['6', '7', '7']}
    True

    >>> x = Table()
    >>> x.set_dict({'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
        'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
        'year': ['5', '5', '5', '6', '6', '6'],
        'y': ['5', '6', '7', '5', '6', '7'],
        'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']})
    >>> greater_column(x, 'title>t')
    >>> x._all_data == {'money': ['1.0'], 'title': ['m2'],
                        't': ['m1'], 'y': ['5'], 'year': ['6']}
    True
    '''
    # getting the list of keys
    list_keys = list(new_table._all_data.keys())

    rows = new_table.num_rows()
    # getting a list of the columns that'll be compared
    list_comparison = where_query.split('>')
    first_column = list_comparison[0]
    second_column = list_comparison[1]

    # this is a list of indexes that will contain any index
    # that should be deleted based on the where constraint
    index_deletion = []

    # tables dictionary is new_table._all_data
    for i in range(rows):
        # checks if the first column value is <= the second column value
        # checks the ith term
        if (new_table._all_data[first_column][i] <= (new_table._all_data
                                                     [second_column][i])):
            index_deletion.append(i)

    # reverses the index of deletion so it will work with .pop()
    # and removes last value
    index_deletion.reverse()

    # check every column and delete the row required from the column
    for i in index_deletion:
        for keys in new_table._all_data:
            useless_value = new_table._all_data[keys].pop(i)

    # getting the list of the new keys to update the row variable
    list_keys = list(new_table._all_data.keys())
    new_table._rows = len(new_table._all_data[list_keys[0]])


def run_query(databases, query):
    '''(Database, str) -> Table
    runs a SQuEaL query on the given databases and returns the resulting
    table

    REQ: databases has the format {'filename':Table}
    REQ: the query is a valid one with appropriate format
    REQ: all databases contain appropriately formatted tables
    '''
    if (query != ''):
        # getting list of tokens
        query_list = query.split(' ', 5)
        # temporary holder value
        where_clause = ''
        # checks if there is in fact a where clause by looking at length
        if (len(query_list) > WHERE_TOKEN):
                for i in range(len(query_list[5].split("\'", 3))):
                    # makes sure to get rid of quotations
                    # within the where clause
                    where_clause = (where_clause +
                                    query_list[5].split("\'", 3)[i])
                # prevents the loop from going to other where clauses
                where_clause = where_clause.rsplit('\'', 1)[0]
                # updates the query list with the value of where_clause
                query_list[5] = where_clause

        # creating a list of all tables
        list_tables = []

        # checking the amount of files to look at - seperated by commas
        files = query_list[FILES_IN_QUERY].split(',')
        # if we are only looking at one file
        if (len(files) == 1):
            table = files[0]
            new_table = databases._all_tables[table]
            list_tables.append(new_table)

        elif (len(files) == 2):
            # case for when user asks to look at two files
            # creates all the requested tables and puts them in a list
            for i in range(len(files)):
                # creating the table
                table = databases._all_tables[files[i]]
                # adding the table to the list of tables
                list_tables.append(table)

            # combining the two tables
            new_table = cartesian_product(list_tables[0], list_tables[1])

        elif (len(files) >= 3):
            # case for when the user asks to look at 3 or more files
            # creates all the requested tables and puts them in a list
            temp_list_tables = []
            for i in range(len(files)):
                # creating the table
                table = databases._all_tables[files[i]]
                # adding the table to the list of tables
                temp_list_tables.append(table)

            # doing cartesian product once
            new_table = cartesian_product(temp_list_tables[0],
                                          temp_list_tables[1])
            list_tables.append(new_table)

            # repeating cartesian product until it is a
            # combination of all tables
            for i in range(2, len(temp_list_tables)):
                list_tables.append(cartesian_product
                                   (new_table, temp_list_tables[i]))
                # chooses the final table in the list
                # which is the updated cartesian product
                new_table = list_tables[-1]

    # checks if there is a where token
    if 'where' in query:
        where_query_list = query_list[WHERE_VALUE].split(',')
        for i in range(len(where_query_list)):
            # determines what type of where query it is
            where_query = which_where_query(where_query_list[i], list_tables)
            if (where_query == COLUMN_EQUAL_VALUE):
                # column_name1='value' comparison
                edit_table = equal_value(new_table, where_query_list[i])
            elif (where_query == COLUMN_EQUAL_COLUMN):
                # column_name1=column_name2 comparison
                edit_table = equal_column(new_table, where_query_list[i])
            elif (where_query == COLUMN_GREATER_VALUE):
                # column_name1>'value' comparison
                edit_table = greater_value(new_table, where_query_list[i])
            elif (where_query == COLUMN_GREATER_COLUMN):
                # column_name1>column_name2 comparison
                edit_table = greater_column(new_table, where_query_list[i])

    # performs the select token to get the final table
    final_table = select_token(query_list, files, new_table)
    return final_table

if(__name__ == "__main__"):
    # reads all files in the directory
    databases = read_database()

    query = input("Enter a SQuEaL query, or a blank line to exit:")

    # continues asking for sQuEaL queries until a blank line is entered
    while (query != ''):
        # applies squeal to get the table
        table = run_query(databases, query)
        # outputting the table
        print_csv(table)
        # takes squeal input from the user
        query = input("Enter a SQuEaL query, or a blank line to exit:")
