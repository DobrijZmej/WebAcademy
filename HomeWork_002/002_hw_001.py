import math

n1 = input('Первое число: ')
n2 = input('Второе число: ')
operator = input('Оператор:').lower()

if(not n1.isdigit()):
    print(f'[{n1}] - это не число')
    break #exit(0)

if(not n2.isdigit()):
    print(f'[{n2}] - это не число')
    exit(0)

if(operator not in ('+', '-', '*', '/', '**', 'sin', 'cos')):
    print(f'[{operator}] - это недопустимый оператор')
    exit(0)

n1 = int(n1)
n2 = int(n2)
if(operator == '+'):
    print(n1+n2)
elif(operator == '-'):
    print(n1-n2)
elif(operator == '*'):
    print(n1*n2)
elif(operator == '/'):
    print(n1/n2)
elif(operator == '**'):
    print(n1**n2)
elif(operator == 'sin'):
    print(operator, n1, '=', math.sin(n1))
    print(operator, n2, '=', math.sin(n2))
elif (operator == 'cos'):
    print(operator, n1, '=', math.cos(n1))
    print(operator, n2, '=', math.cos(n2))
