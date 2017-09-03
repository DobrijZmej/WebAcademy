def check_data(in_data):
    if in_data.isdigit():
        return True
    return False

def is_prime(in_number):
    for i in range(2, in_number):
        if in_number % i == 0:
            return i
    return 0

def main():
    data = input('Введите число: ')
    if check_data(data):
        data = int(data)
        result = is_prime(data)
        if result == 0:
            print('Это простое число')
        else:
            print(f'Это сложное число, оно делится как минимум на {result}')
    else:
        print(f'[{data}] не является корректным числом')

if __name__ == '__main__':
    main()