# Functions for reading tables and databases

import glob
from database import *

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.
# Write the read_table and read_database functions below


def read_table(file_open):
    ''''(str) -> Table
    Takes in a file name, reads the file and places it into a Table with
    appropriate formatting

    REQ: the file name is valid
    REQ: the file is formatted properly
    REQ: the file is a .csv file
    '''
    my_file = open(file_open, "r")
    # holder values for columns and rows
    titles = []
    list_of_columns = []

    # gets a list of all the lines within the file
    all_lines = my_file.readlines()

    # closing file as it is no longer needed
    my_file.close()

    # gets the titles from the first line of the file
    # removes any blank space
    all_lines[0] = all_lines[0].strip()
    # splits the columns into a list
    titles = all_lines[0].split(",")

    # strips any newlines
    for i in range(1, len(all_lines)):
        all_lines[i] = all_lines[i].strip()

    # gets a list that holds lists pertaining to each column
    # i.e [title[title1,title2]]
    # it starts at 1 because the first line was already read
    for i in range(1, len(titles)+1):
        # sets a temporary variable to hold a column
        # this value constantly resets per column created
        columns = []
        # adds the first value in the all_lines
        # starts from 1 because the first was already read
        for j in range(1, len(all_lines)):
            # makes sure it doesn't read lines that aren't there
            if (len(all_lines[j]) > 0):
                # creates a list for the column (years/titles)
                # seperates each item using the comma
                # also strips any blank spaces left
                columns.append((all_lines[j].split(",")[i-1]).strip())

        # puts together the column in a list of columns
        list_of_columns.append(columns)

    # creates a table and fills it with the data from the file
    table = Table()
    table.table_data(titles, list_of_columns)

    return table


# A database is a dict of {str:table},
# where the keys are table names and values are the tables.
def read_database():
    '''() -> Database
    reads all files within the directory and returns a Database
    containing all the tables of said directory
    REQ: the directory contains at least one file
    REQ: files can only contain one .csv, can't be of the form
    filename.csv.csv
    '''
    # gets a list of all the files within the directory
    file_list = glob.glob('*.csv')

    # list containing all the tables of each file of the directory
    table_list = []

    # list containing all the titles of the directory
    title_list = []

    # getting the titles of the directory
    for i in range(len(file_list)):
        title_list.append(file_list[i].replace('.csv', ''))

    # getting all the tables for each file
    for i in range(len(file_list)):
        # getting the table for the file
        file_table = read_table(file_list[i])
        table_list.append(file_table)

    # Creating a Database containing all the files
    data = Database()

    # filling in the database with information
    data.database_data(title_list, table_list)

    return data
