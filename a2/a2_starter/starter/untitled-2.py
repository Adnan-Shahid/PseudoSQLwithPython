def read_table(file_name):
    filehandler = open(file_name, "r")
    column_list = []
    rows_list = []
    list_lines = filehandler.readlines()
    filehandler.close()
    list_lines[0] = list_lines[0].strip()
    column_list = list_lines[0].split(",", -1)
    for i in range(1, len(list_lines)):
        list_lines[i] = list_lines[i].strip()
    for i in range(1, len(column_list)+1):
        list_lines[i] = list_lines[i].strip()
        whole_column_list = []
        for counter in range(1,len(list_lines)):
            if (len(list_lines[counter]) > 0):
                whole_column_list.append(list_lines[counter].split(",",-1)[i-1])
        rows_list.append(whole_column_list)
    print("adnan is a fgt")
    print(list_lines)
    return Table_obj
read_table('books.csv')