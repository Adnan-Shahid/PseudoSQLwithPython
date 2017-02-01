def read_table(file_name):    
    filehandler = open(file_name, "r")
    column_list = []
    rows_list = []
    list_lines = filehandler.readlines()
    filehandler.close()
    list_lines[0] = list_lines[0].strip()
    column_list = list_lines[0].split(",")



    for i in range(1, len(column_list)+1):
        list_lines[i] = list_lines[i].strip()
        whole_column_list = []
        for counter in range(1,len(list_lines)):
            if(list_lines[counter] != ''):
                whole_column_list.append(list_lines[counter].split(", ")[i-1])
        rows_list.append(whole_column_list)
    print(rows_list)
    print(column_list)
read_table('books.csv')

    #Table_obj = Table(column_list, rows_list)

    #return Table_obj