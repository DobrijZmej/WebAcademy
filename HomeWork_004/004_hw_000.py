def my_max(*in_list):
    current_max = None
    for i in in_list:
        if current_max is None:
            current_max = i
        if i > current_max:
            current_max = i
    #print(in_list)
    #print(current_max)
    return current_max

def my_max_sort(*in_list):
    list = [i for i in in_list]
    list.sort()
    return list[-1]

def my_min(*in_list):
    current_max = None
    for i in in_list:
        if current_max is None:
            current_max = i
        if i < current_max:
            current_max = i
    #print(in_list)
    #print(current_max)
    return current_max

def my_min_sort(*in_list):
    list = [i for i in in_list]
    list.sort(reverse=True)
    return list[-1]

numbers = (4,6,7,8, 54654, 654654, 54, 6546, -121)

print(my_max(*numbers))
print(my_max_sort(*numbers))

print(my_min(*numbers))
print(my_min_sort(*numbers))

