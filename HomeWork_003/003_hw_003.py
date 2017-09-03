def is_even(in_number):
    if in_number % 2 == 0:
        return True
    return False

def main():
    even_counter = 0
    current_number = 1
    while even_counter < 10:
        if is_even(current_number):
            print(f'{current_number} это четное число номер {even_counter+1}')
            even_counter += 1
        current_number += 1

if __name__ == '__main__':
    main()