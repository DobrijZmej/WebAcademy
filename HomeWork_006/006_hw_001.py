CURRENT_YEAR = 2017

class ShowRoomError(ValueError):
    pass

class CarNotFoundError(ShowRoomError):
    pass

class Car:
    def __init__(self, in_mark, in_year, in_price, in_color):
        if in_year > CURRENT_YEAR:
            raise ValueError('Машина не может быть из будущего!')
        if in_price <= 0:
            raise ValueError('Стоимость машины не может быть меньше или равно нулю!')
        self.mark = in_mark
        self.year = in_year
        self.price = in_price
        self.color = in_color
    def __str__(self):
        return f'Марка {self.mark}, {self.year} года выпуска, стоимостью ${self.price}'


class ShowRoom:
    def __init__(self, in_address, in_name):
        self.address = in_address
        self.name = in_name
        self.cars = []

    def add_car(self, in_car):
        self.cars.append(in_car)

    def buy_car(self, in_car):
        if(in_car in self.cars):
            self.cars.remove(in_car)
        else:
            raise CarNotFoundError('Требуемая машина не найдена в салоне, для продажи необходимо выполнить предзаказ.')

    def is_car_exists(self, in_car):
        if(in_car in self.cars):
            return True
        else:
            return False

    def show_all_card(self):
        print(f'В салоне на текущий момент находится {len(self.cars)} автомобилей')
        mark_len = max(len(i.mark) for i in self.cars)
        color_len = max(len(i.color) for i in self.cars)
        year_len = max(len(str(i.year)) for i in self.cars)
        price_len = max(len(str(i.price)) for i in self.cars)
        num_len = len(str(len(self.cars)))
        for i, car in enumerate(self.cars):
            print(f'|{str(i).rjust(num_len)}|'
                  f'{car.mark.ljust(mark_len)}|'
                  f'{car.color.ljust(color_len)}|'
                  f'{str(car.year).rjust(year_len)}|'
                  f'${str(car.price).rjust(price_len)}|')

def main():
    show_room = ShowRoom('Kiev', 'Salon1')

    car1 = Car('BMW', 2010, 15000, 'Red')
    car2 = Car('audi', 2015, 18000, 'Black')
    car3 = Car('Lanos', 2016, 8000, 'Gray')

    show_room.add_car(car1)
    show_room.add_car(car2)
    show_room.add_car(car3)
    show_room.show_all_card()

    print('')
    print(f'Продаю машину {car2}')
    print('')
    show_room.buy_car(car2)
    show_room.show_all_card()

    print('')
    car4 = Car('Subaru', 2016, 8000, 'Gray')
    if(show_room.is_car_exists(car4)):
        print(f'Машина [{car4}] доступна для продажи')
    else:
        print(f'Машина [{car4}] на текущий момент отсутствует, необходим предзаказ')



if __name__ == '__main__':
    main()