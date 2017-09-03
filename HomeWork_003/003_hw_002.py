def check_data(in_data):
    if(in_data.isdigit()):
        return True
    return False

def is_prime(in_number):
    for i in range(2, in_number):
        if in_number % i == 0:
            return i
    return 0

def main():
    prime_counter = 0
    current_number = 1
    while prime_counter < 10:
        if(is_prime(current_number) == 0):
            print(f'{current_number} это простое число номер {prime_counter+1}')
            prime_counter += 1
        current_number += 1

if __name__ == '__main__':
    main()