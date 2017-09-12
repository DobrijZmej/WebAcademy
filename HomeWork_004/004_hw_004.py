import random

def sort_radix(in_num_list):
    def sort_insert(numbers):
        sort_numbers = []
            # пока массив не закончится, продолжаем интерации
        while len(numbers) > 0:
            min_number, min_position = None, None
                # бежим по массиву, определяя самое меньшее число
            for r in range(len(numbers)):
                if(min_number is None):
                    min_number = numbers[r]
                    min_position = r
                if(numbers[r] < min_number):
                    min_number = numbers[r]
                    min_position = r
                # наименьшее число определено - добавим его в результат
                # и удалим из входящего массива чисел
            sort_numbers.append(min_number)
            del numbers[min_position]
        return sort_numbers

        # создали словарь, и загоняем в словарь цифры в зависимости от количества символов
    dict_on_digits = {}
    for i in in_num_list:
        digit_len = len(str(i))
        if digit_len not in dict_on_digits.keys():
            dict_on_digits[digit_len] = []
        dict_on_digits[digit_len].append(i)
    #print(dict_on_digits)
        # есть словарь, в котором ключи это цифры (количество разрядов) - отсортируем их как обычные цифры
    sorted_keys = sort_insert(list(dict_on_digits.keys()))
    result = []
        # теперь отсортируем сами значения для каждого из ключей, и склеим, так как ключи у нас уже в нужном порядке расположены
    for r in sorted_keys:
        result += sort_insert(dict_on_digits[r])
    return result

def main():
    #num_list = [1, 654, 321, 21, 4564, 4654, 8, 1321]
    num_list = [random.randint(1, 9999) for _ in range(100)]
    print(num_list)
    print(sort_radix(num_list))

if __name__ == '__main__':
    main()