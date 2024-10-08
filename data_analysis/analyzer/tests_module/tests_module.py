import unittest
import numpy as np 
import pandas as pd 
from analyzer.functions_for_analysis.functions_module import TimerowForAnalise

class TestTimerowForAnalise(unittest.TestCase):

    def setUp(self):
        # Инициализация объекта с тестовыми данными
        self.data = np.array([1, 2, 3, 2, 1, 2, 3])
        self.analiz = TimerowForAnalise(self.data)

    def test_calculate_moving_average(self):
        #проверка функции подсчета среднего скользящего
        expected_result = pd.Series([np.nan, np.nan, 2.0, 2.333333, 2.0, 1.666667, 2.0])
        result = self.analiz.calculate_moving_average(window_size=3)

        # Используем генератор для проверки значений
        for i, (expected, actual) in enumerate(zip(expected_result, result)):
            if np.isnan(expected) and np.isnan(actual):
                # Если оба значения NaN, то тест проходит
                continue 
            else:
                self.assertAlmostEqual(expected, actual, places=5, msg=f"Ошибка в позиции {i}")

    def test_calculate_differential(self):
        #проверка функции вычисления дифференциала
        expected_result = pd.Series([np.nan, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0])
        result = self.analiz.calculate_differential()

        # Используем генератор для проверки значений
        for i, (expected, actual) in enumerate(zip(expected_result, result)):
             # Проверяем, является ли значение NaN 
            if np.isnan(expected) and np.isnan(actual):
            # Если оба значения NaN, то тест проходит
               continue 
            else:
                self.assertAlmostEqual(expected, actual, places=5, msg=f"Ошибка в позиции {i}")
        

    def test_calculate_autocorrelation(self):
        #проверка функции посчета автокорреляции
        expected_result = pd.Series([0.058824]) 
        result = self.analiz.calculate_autocorrelation(lag=1)
        pd.testing.assert_series_equal(result, expected_result, check_exact=False, check_index=False, check_dtype=False)

    def test_find_maxime(self):
        #проверка функции нахождения минимумов
        expected_result = pd.Series([3], index=[2])
        result = self.analiz.find_maxime()
        pd.testing.assert_series_equal(result, expected_result)

    def test_find_minimum(self):
        #проверка функции нахождения максимумов
        expected_result = pd.Series([1], index=[4])
        result = self.analiz.find_minimum()
        self.assertTrue(result.equals(expected_result))
    
    def test_decompose_time_series_multiplicative(self):
         # Создаем тестовый DataFrame с 20 значениями
        data = np.array([1, 2, 3, 2, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6])
        data_series = pd.Series(data, index=pd.date_range(start='2023-01-01', periods=len(data), freq='D'))
        df = pd.DataFrame({'value': data_series})

        # Создаем объект TimerowForAnalise
        ts = TimerowForAnalise(df['value'])

        # Выполняем разложение с моделью 'multiplicative'
        decomposed_df = ts.decompose_time_series(model='multiplicative')

        # Проверяем, что DataFrame имеет правильное количество столбцов
        self.assertEqual(len(decomposed_df.columns), 3)

        # Проверяем, что значения в столбцах имеют правильный тип
        self.assertTrue(all(isinstance(x, (float, pd.NA)) for x in decomposed_df['Trend'].values))
        self.assertTrue(all(isinstance(x, (float, pd.NA)) for x in decomposed_df['Seasonal'].values))
        self.assertTrue(all(isinstance(x, (float, pd.NA)) for x in decomposed_df['Residual'].values))
    

