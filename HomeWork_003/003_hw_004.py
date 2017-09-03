def input_data():
    figure = input('Выберите фигуру:\r\n'
                   '1. Квадрат\r\n'
                   '2. Треугольник\r\n'
                   '3. Ромб\r\n').lower()
    n1 = input('Укажите ширину: ')
    n2 = input('Укажите высоту: ')
    return [n1, n2, figure]

def check_data(in_data):
    if in_data[2] not in ('1', '2', '3'):
        return -1
    if not in_data[0].isdigit():
        return -2
    if not in_data[1].isdigit():
        return -3
    return 0

def paint_romb(width, height):
    for h in range(1, height + 1):
        print(' ' * round(width * (height - h) / height), end='')
        print('*' * round(width * h / height), end='')
        print('*' * round(width * h / height))
    for h in range(1, height + 1):
        print(' ' * round(width * (height - (height - h)) / height), end='')
        print('*' * round(width * (height - h) / height), end='')
        print('*' * round(width * (height - h) / height))

def paint_kvadrat(width, height):
    for h in range(height):
        print('*' * width)

def paint_treugol(width, height):
    for h in range(1, height + 1):
        # print(' ' * round(width * (height - h) / height), end='')
        print('*' * round(width * h / height))


def main():
    data = input_data()
    check_result = check_data(data)
    if check_result < 0:
        if check_result == -1:
            print('Ошибка выбора фигуры')
        elif check_result == -2:
            print(f"[{data[0]}] - это не число")
        elif check_result == -3:
            print(f"[{data[1]}] - это не число")
        else:
            print('Другая ошибка')
    else:
        figure = int(data[2])
        width = int(data[0])
        height = int(data[1])
        if figure == 1:
            paint_kvadrat(width, height)
        elif figure == 2:
            paint_treugol(width, height)
        else:
            paint_romb(width, height)

if __name__ == '__main__':
    main()