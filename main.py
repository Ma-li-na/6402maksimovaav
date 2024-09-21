import argparse
import math

def read_data(filename: str) -> dict:
    """Загружает параметры из текстового файла.

    Аргументы:
    filename (str): Путь к текстовому файлу, содержащему параметры.

    Возвращает:
    dict: Словарь с параметрами, где ключами являются имена параметров,
    а значениями — числовые значения (int или float).
    """
    dict_of_number = {}
    
    with open(filename, 'r') as file:
         for line in file:
            line = line.strip()  # Удаляем лишние пробелы и символы новой строки
            if '=' in line:
                key, value = line.split('=', 1)  # Разделяем строку по первому вхождению '='
                dict_of_number[key.strip()] = float(value.strip())  # Сохраняем в словарь, удаляя пробелы, преобразуем число из str в float
    
    return dict_of_number

def factorial(n: int) -> int:
    """Вычисляет факториал числа n.

    Аргументы: 
    n (int) - неотрицательное целое число.

    Возвращает: 
    result (int) - факториал n."""
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def cosine(x: float, terms: int = 10) -> float:
    """Вычисляет косинус x с использованием ряда Тейлора.

    Аргументы: 
    x (float) - угол в радианах.
    terms (int) - количество членов ряда для вычисления (по умолч. 10).

    Возвращает: 
    result (float) - Значение косинуса угла x. """

    result = 0
    for n in range(terms):
        sign = (-1) ** n  # Знак члена ряда
        result += sign * (x ** (2 * n)) / factorial(2 * n)  # Член ряда Тейлора
    return result

def normalize_angle(x: float) -> float:
    """Нормализует угол x в диапазоне [0, 2π).

    Аргументы: 
    x (float) - угол в радианах.

    Возвращает: 
    х (float) - нормализованный угол."""

    while x < 0:
        x += 2 * math.pi  
    while x >= 2 * math.pi:
        x -= 2 * math.pi 
    return x

def cos_bx_c(b: float, x: float, c: float) -> float:
    """Вычисляет косинус bx + c.

    Аргументы: 
    b (float) - коэффициент b, 
    x (float) - угол, 
    c (float) - константа c.

    Возвращает: 
    значение функции cosine (float) - значение косинуса угла b*x+c."""

    angle = b * x + c
    normalized_angle = normalize_angle(angle)
    return cosine(normalized_angle)

def numerator(b: float, x: float, c: float) -> float:
    """Вычисляет числитель функции.
    
    Аргументы: 
    b (float) - коэффициент b,
    x (float) - угол, 
    c (float) - константа c.

    Возвращает: 
    cos_value (float) - значение числителя дроби."""

    cos_value = cos_bx_c(b, x, c)  
    cos_value = cos_value ** 4  
    cos_value += 1
    return cos_value

def denominator(x: float) -> float:
    """Вычисляет знаменатель функции.
    
    Аргументы: 
    x (float) - угол.

    Возвращает: 
    тип float - значение знаменателя дроби."""

    return 3 + x

def function_result_at_point(a: float, b: float, c: float, x: float) -> float:
    """Вычисляет значение функции для заданных параметров (т.е. в конкретной точке). 

    Аргументы: 
    a (float) - коэффициент a, 
    b (float) - коэффициент b, 
    c (float) - константа c, 
    x (float) - угол.

    Возвращает: 
    тип float - значение функции в x при заданных коэффициентах."""

    return a * numerator(b, x, c) / denominator(x)

def save_data(filename: str, data: list[float], sep: str) -> None:
    """Сохраняет данные в файл с заданным разделителем.
    
    Аргументы: 
    filename (str) - имя файла, 
    data (список элементов типа (float)) - список данных, 
    sep (str) - разделитель.
    
    Возвращает:None"""

    with open(filename, 'w') as file:
        file.write(sep.join(map(str, data)))  # Преобразуем элементы в строки


parser = argparse.ArgumentParser(description="Вычисление функции y(x) и запись результатов в файл.")
# Параметры, которые можно передать через командную строку
parser.add_argument("--config", type=str, default="config.txt")
parser.add_argument("--n0", type=float)
parser.add_argument("--h", type=float)
parser.add_argument("--nk", type=float)
parser.add_argument("--a", type=float)
parser.add_argument("--b", type=float)
parser.add_argument("--c", type=float)
    
args = parser.parse_args()

# Чтение параметров из файла
params = read_data(args.config)
n0 = args.n0 if args.n0 is not None else params['n0']
h = args.h if args.h is not None else params['h']
nk = args.nk if args.nk is not None else params['nk']
a = args.a if args.a is not None else params['a']
b = args.b if args.b is not None else params['b']
c = args.c if args.c is not None else params['c']

list_of_number = []

while n0 <= nk:
    list_of_number.append(function_result_at_point(a, b, c, n0))  
    n0 += h

print(list_of_number)
save_data("output.txt", list_of_number, sep=", ")















