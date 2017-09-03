width  = 20
height = 10
steps  = 3

print('Ромб:')
for h in range(1, height+1):
    print(' '*round(width*(height-h)/height), end='')
    print('*'*round(width*h/height),          end='')
    print('*'*round(width*h/height)                 )
for h in range(1, height + 1):
    print(' '*round(width*(height-(height-h))/height), end='')
    print('*' * round(width * (height-h) / height),    end='')
    print('*' * round(width * (height-h) / height)           )

print('Елочка:')
for i in range(steps):
    for h in range(1, height + 1):
        print(' ' * round(width * (height - h) / height), end='')
        print('*' * round(width * h / height), end='')
        print('*' * round(width * h / height))

print('Треугольник:')
for h in range(1, height + 1):
    #print(' ' * round(width * (height - h) / height), end='')
    print('*' * round(width * h / height))

print('Квадрат:')
for h in range(height):
    print('*'*height)

print('Ступеньки:')
#step_prev = -1;
for i in range(steps):
    print((' '*round(width*((i)/steps)))+'*', end='')
    print('*'*round(width*(1/steps)))
    for h in range(height):
        print((' '*round(width*((i+1)/steps)))+'*')
