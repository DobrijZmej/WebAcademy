def check_data(in_data):
    if in_data.isdigit():
        return True
    return False

def get_digits_count(in_number):
    digits_count = 0
    edge_number = 1
    while edge_number <= in_number:
        digits_count += 1
        edge_number *= 10
    return digits_count

def main():
    data = input('Введите число: ')
    if check_data(data):
        data = int(data)
        result = get_digits_count(data)
        print(f'Размерность числа {data} равна {result}')
    else:
        print(f'[{data}] не является корректным числом')

if __name__ == '__main__':
    main()