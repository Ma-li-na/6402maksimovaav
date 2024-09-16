def read_data(filename):
    """Читает данные из файла.

    Название файла передается как аргумент функции.
    Возвращает список чисел (типа float)."""

    lst = []
    number = ""
    
    with open(filename, 'r') as file:
        for line in file:
            for char in line:
                if char.isdigit() or char == '-' or char == '.':  
                    number += char
                else:
                    if number:
                        lst.append(float(number))  
                        number = ""
            if number:  
                lst.append(float(number))  

    return lst


def factorial(n):
  
    """Вычисляет факториал числа n.

    Аргумент - число n (неотрицательное, целое).
    Возвращает факториал n."""

    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def cosine(x, terms=10):
    """Вычисляет косинус угла x с использованием ряда Тейлора.

    Аргументы: угол, terms - количество членов ряда для вычисления (по умолч 10).
    Возвращает - значение косинуса угла х."""

    result = 0
    for n in range(terms):
        sign = (-1) ** n  # Знак члена ряда
        result += sign * (x ** (2 * n)) / factorial(2 * n)  # Член ряда Тейлора
    return result

def normalize_angle(x):
    """Нормализует угол x в диапазоне [0, 2Pi].

    Аргумент - угол в радианах.
    Возвращает - нормализованный угол"""

    while x < 0:
        x += 2 * 3.141592653589793  
    while x >= 2 * 3.141592653589793:
        x -= 2 * 3.141592653589793 
    return x

def cos_bx_c(b,x,c):
    """Вычисляет косинус угла b*x+c.

    Аргументы: угол, значения коэффициентов.
    Возвращает - значение косинуса угла b*x+c"""

    # Вычисляем угол b*x + c
    angle = b * x + c
    # Нормализуем угол
    normalized_angle = normalize_angle(angle)
    # Вычисляем косинус
    return cosine(normalized_angle)


def numerator(b, x, c):
    """ Считаем числитель дроби

    Аргументы - угол, значения коэффициентов.
    Возвращает значение числителя дроби."""

    cos_value = cos_bx_c(b, x, c)  
    cos_value = cos_value ** 4  
    cos_value += 1
    return cos_value


def denominator(x):
    """Считаем знаменатель дроби.

    Аргумент - угол.
    Возвращает значение знаменателя дроби."""
    return 3 + x


def function(a, b, c, x):
    """Считаем значение функции.

    Аргументы: коэффициенты, угол.
    Возвращает значение функции в x при заданных коэффициентах."""

    return a * numerator(b, x, c) / denominator(x)

def save_data(filename, data, sep):
    """Сохраняем данные в файл.

    Аргументы - имя файла, список данных, разделитель."""

    with open(filename, 'w') as file:
        file.write(sep.join(map(str, data)))  # Преобразуем элементы в строки


answer = input('Do you want to enter data from the config.txt file (Y) or from the console (N)? ')
while answer != 'Y' and answer != 'N':
    answer = input('You are wrong. Try again (Y/N): ')

if answer == 'Y':
    list_of_number = read_data("config.txt")
elif answer == 'N':
    print('Enter the data in the following order n_0, h, n_k, a, b, c separated by spaces: ')
    list_of_number = []
    # Считываем данные с консоли и добавляем их в список
    data = input().split()
    list_of_number = [float(num) for num in data]  # Преобразуем введенные данные в числа

n_0 = list_of_number[0]
h = list_of_number[1]
n_k = list_of_number[2]
a = list_of_number[3]
b = list_of_number[4]
c = list_of_number[5]
list_of_number.clear()

while n_0 <= n_k:
    list_of_number.append(function(a, b, c, n_0))  
    n_0 += h

print(list_of_number)
save_data("output.txt", list_of_number, sep=", ")