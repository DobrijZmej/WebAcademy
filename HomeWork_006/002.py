CURRENT_YEAR = 2017

class Car:
    def __init__(self, in_mark, in_year, in_price):
        if in_year > CURRENT_YEAR:
            raise ValueError('Машина не может быть из будущего!')
        if in_price <= 0:
            raise ValueError('Стоимость машины не может быть меньше или равно нулю!')
        self.mark = in_mark
        self.year = in_year
        self.price = in_price
    def __str__(self):
        return f'Марка {self.mark}, {self.year} года выпуска, стоимостью ${self.price}'

def is_one_more():
    responce = input('Продолжаем?(y/n): ').lower()
    if responce != 'y':
        return False
    return True

def main():
    container = []
    while True:
        model = input('Модель: ')
        try:
            year = int(input('Год выпуска: '))
        except ValueError:
            print('Неверное значение года, введите целое цифровое значение')
            continue
        try:
            price = float(input('Стоимость: '))
        except ValueError:
            print('Неверная стоимость, введите числовое значение')
            continue
        try:
            car = Car(model, year, price)
        except ValueError as excpt:
            print('Ошибка!', excpt)
            continue

        container.append(car)
        print()
        print('В контейнере уже есть такие машины:')
        for car in container:
            print(car)

        if not is_one_more():
            break


if __name__ == '__main__':
    main()