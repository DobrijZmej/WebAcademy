n1 = int(input('Первое число: '))
n2 = int(input('Второе число: '))
n3 = int(input('Третье число: '))

if(n1 == n2 or n2 == n3 or n1 == n3):
    print(n1+5)
    print(n2+5)
    print(n3+5)
else:
    print('равных нет')