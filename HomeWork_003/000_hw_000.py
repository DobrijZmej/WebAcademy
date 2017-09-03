import math

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def pow(a, b):
    return a ** b

def div(a, b):
    if(b == 0):
        return(None)
    else:
        return a / b

def sin(a):
    return math.sin(a)

def cos(a):
    return math.cos(a)

def input_data():
    n1 = input('Первое число: ')
    n2 = input('Второе число: ')
    operator = input('Оператор:').lower()
    return [n1, n2, operator]

def check_data(in_data):
    if not in_data[0].isdigit():
        return -1
    if not in_data[1].isdigit():
        return -2
    if (in_data[2] not in ('+', '-', '*', '/', '**', 'sin', 'cos')):
        return -3
    return 0

def do_action(n1, n2, operator):
    if(operator == '+'):
        return add(n1, n2)
    if(operator == '-'):
        return sub(n1, n2)
    if(operator == '*'):
        return mul(n1, n2)
    if(operator == '**'):
        return pow(n1, n2)
    if(operator == '/'):
        return div(n1, n2)
    if(operator == 'sin'):
        return (sin(n1), sin(n2))
    if(operator == 'cos'):
        return (cos(n1), cos(n2))

def main():
    is_first_loop = True
    while True:
        if(not is_first_loop):
            user_responce = None
            while user_responce not in ('y', 'n'):
                user_responce = input('Ещё раз?(y/n) ').lower()
            if user_responce == 'n':
                break
        is_first_loop = False

        data = input_data()
        check_result = check_data(data)
        if(check_result<0):
            if(check_result == -1):
                print(f"[{data[0]}] - это не число")
            elif(check_result == -2):
                print(f"[{data[1]}] - это не число")
            elif(check_result == -3):
                print(f'[{data[2]}] - это недопустимый оператор')

        n1 = int(data[0])
        n2 = int(data[1])
        operator = data[2]

        result = do_action(n1, n2, operator)
        print(result)


if __name__ == '__main__':
    main()