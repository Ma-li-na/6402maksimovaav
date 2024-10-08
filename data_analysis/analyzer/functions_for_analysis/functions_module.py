import numpy as np 
import pandas as pd
from typing import Any, Callable
from statsmodels.tsa.seasonal import seasonal_decompose

def decorator(func : Callable) -> Callable:
    # Простой декоратор для логирования вызовов функций
    def wrapper(*args : Any, **kwargs : Any):
        print(f"Вызов функции: {func.__name__} с аргументами: {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"Результат: {result}")
        return result
    return wrapper 

class TimerowForAnalise:
    
    def __init__(self, data : np.ndarray) -> None:
        """ Инициализация класса с временным рядом

        Аргументы: 
        data (np.ndarray) - массив данных для инициализации временного ряда
        """
        self.data = pd.Series(data)
    
    @decorator
    def calculate_moving_average(self, window_size: int = 3) -> pd.Series:
        """Подсчет скользящего среднего для временного ряда.

        Аргументы: 
        window_size (int) - размер окна для скользящего среднего.
        
        Возвращает:
        pd.Series - скользящее среднее временного ряда.
        """
        return self.data.rolling(window=window_size).mean()
    

    @decorator
    def calculate_differential(self) -> pd.Series:
        """ Вычисление дифференциала для временного ряда
        Возвращает:
        pd.Series - дифференциал временного ряда"""

        return self.data.diff()

    @decorator
    def calculate_autocorrelation(self, lag: int = 1) -> pd.Series:
        """ Вычисление автокорреляции временного ряда
        
        Аргументы: 
         lag (int) - лаг для вычисления автокорреляции
        
        Возвращает: 
        pd.Series - значение автокорреляции"""
        
        # Вычисление автокорреляции
        autocorr = self.data.autocorr(lag)
        return pd.Series(autocorr)
        
        
       

    @decorator 
    def find_maxime(self) -> pd.Series:
        """ Поиск максимумов временного ряда

        Возвращает:
        pd.Series - возвращает локальные максимумы
        """
        return self.data[(self.data.shift(1) < self.data) & (self.data.shift(-1) < self.data)]

    @decorator
    def find_minimum(self) -> pd.Series:
        """Поиск минимумов временного ряда

        Возвращает: 
        pd.Series - возвращает локальные минимумы
        """

        return self.data[(self.data.shift(1) > self.data) & (self.data.shift(-1) > self.data)]

    @decorator 
    def decompose_time_series(self, model='additive', period=None) -> pd.DataFrame:
        decomposed = seasonal_decompose(self.data, model=model, period=period)
        trend = decomposed.trend
        seasonal = decomposed.seasonal
        residual = decomposed.resid
        
        results_df = pd.DataFrame({
            'Trend': trend,
            'Seasonal': seasonal,
            'Residual': residual
         })
        return results_df

    @decorator
    def save_to_dataframe(self, result: pd.Series, name: str) -> pd.DataFrame:
      """Сохраняет результат вычислений в DataFrame с заданным именем столбца.

      Аргументы:
      result (pd.Series) - результат вычислений.
      name (str) - имя столбца для результата в DataFrame.

      Возвращает:
      pd.DataFrame - DataFrame с результатами.
      """
      return pd.DataFrame({name: result})
      

    def get_results(self) -> pd.DataFrame:
      """Возвращает DataFrame со всеми результатами анализа."""
      df = self.save_to_dataframe(self.data, 'Temperature')
      
      # Используем цикл для объединения результатов
      for func_name, func in [
          ('Moving average', self.calculate_moving_average),
          ('Differential', self.calculate_differential),
          ('Autocorrelation', self.calculate_autocorrelation),
          ('Max', self.find_maxime),
          ('Min', self.find_minimum),
      ]:
        df = df.join(self.save_to_dataframe(func(), func_name), how='outer')
      decomposed_df = self.decompose_time_series(period=12)
      df = df.merge(decomposed_df, how='outer', left_index=True, right_index=True, suffixes=('Original', 'Decomposed'))
      return df
