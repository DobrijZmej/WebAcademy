import random

def gen_list(in_size):
    def gen_sublist(in_size):
        return [random.randint(100, 999) for _ in range(in_size)]
    return [gen_sublist(in_size) for _ in range(in_size)]

print(gen_list(3))