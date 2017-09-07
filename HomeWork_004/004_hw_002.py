def print_list(in_lists):
    col_sizes = []
    for one_list in in_lists:
        for i, val in enumerate(one_list):
            if(len(col_sizes) <= i):
                col_sizes.append(0)
            col_sizes[i] = max(col_sizes[i], len(str(val)))
    #print(col_sizes)
    buff = ''
    for one_list in in_lists:
        for i, val in enumerate(one_list):
            buff += '| '+str(val).rjust(col_sizes[i])+' '
        buff += '|\r\n'
    print(buff)


print_list([[1,234,3, 3423423434], [5,6,753455, 342]])
