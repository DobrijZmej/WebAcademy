import functools

def check_data(in_data):
    if in_data.isdigit():
        return True
    return False

@functools.lru_cache()
def fib(n):
    if n == 1 or n == 2:  # условие выхода
        return 1
    else:
        return fib(n - 1) + fib(n - 2)  # рекурсивный вызов


def main():
    data = input('Введите число: ')
    if check_data(data):
        data = int(data)
        result = fib(data)
        print(f'{result} - это число Фиббоначи под номером {data}')
    else:
        print(f'[{data}] не является корректным числом')

if __name__ == '__main__':
    main()