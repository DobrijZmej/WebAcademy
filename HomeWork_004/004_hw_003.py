import random

def gen_lists(in_size):
    def gen_sublist(in_size):
        return [random.randint(100, 999) for _ in range(in_size)]
    return [gen_sublist(in_size) for _ in range(in_size)]

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
    buff = buff[:-2]
    print(buff)

def clear_diagonal(in_lists):
    for i in range(len(in_lists)):
        in_lists[i][i] = 0

def normalise(in_lists):
    for list in in_lists:
        for i, val in enumerate(list):
            if val % 2 == 0:
                list[i] = 1
            else:
                list[i] = 0

def get_max_row(in_lists):
    row_sum = []
    for i, list in enumerate(in_lists):
        row_sum.append(sum(list))
    max_row = None
    max_value = -1
    for i, val in enumerate(row_sum):
        if(val > max_value):
            max_row = i
            max_value = val
    #print(row_sum)
    return [in_lists[max_row], max_row+1, max_value]

def rotate(in_lists):
    new_lists = gen_lists(len(in_lists))

    for i, one_list in enumerate(in_lists):
        for j, val in enumerate(one_list):
            new_lists[j][len(one_list)-i-1] = in_lists[i][j]

    return new_lists


def main():
    my_lists = gen_lists(10)

    print('Исходная матрица:')
    print_list(my_lists)

    print('')
    print('Очистим диагональ:')
    clear_diagonal(my_lists)
    print_list(my_lists)

    print('')
    print('Нормализация чёт/нечет:')
    normalise(my_lists)
    print_list(my_lists)

    print('')
    print('Ряд с максимальной суммой:')
    max_row_info = get_max_row(my_lists)
    print(f'{max_row_info[0]} - ряд под номером {max_row_info[1]} на общую сумму {max_row_info[2]}')

    print('')
    print('Развёрнутый ряд:')
    print_list(rotate(my_lists))



if __name__ == '__main__':
    main()
    