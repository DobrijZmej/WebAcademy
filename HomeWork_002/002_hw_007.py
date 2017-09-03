fio = input('Ваше ФИО: ')
group_num = input('Номер группы: ')

str1 = 'Лабораторная работа № 1'
str2 = 'Выполнил(а): ст. гр. '+group_num
str3 = fio

max_len = max((len(str1), len(str2), len(str3)))

print('*'*(max_len+2))
print('*'+str1.ljust(max_len, ' ')+'*')
print('*'+str2.ljust(max_len, ' ')+'*')
print('*'+str3.ljust(max_len, ' ')+'*')
print('*'*(max_len+2))
