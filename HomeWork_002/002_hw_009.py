import random

my_number = random.randint(1, 100)

#print(my_number)

user_number = int(input('Я загадал число от 1 до 100. Попробуй угадай.\r\nТвоё предположение: '))

while user_number != my_number:
    if my_number < user_number:
        print('Слишком много, попробуйте меньше')
    else:
        print('Слишком мало, попробуйте больше')
    user_number = int(input('Новое предположение: '))

print('Правильно,', my_number)