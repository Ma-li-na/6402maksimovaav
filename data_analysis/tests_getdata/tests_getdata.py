import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from getdata import WeatherData  


class TestWeatherData(unittest.TestCase):

    @patch('meteostat.Daily')
    @patch('logging.info')
    def test_get_weather_data_success(self, mock_logging_info, mock_daily):
        # Настройка
        location = (40.7128, -74.0060)  # Пример координат (Нью-Йорк)
        start_date = '2023-01-01'
        end_date = '2023-01-10'
        
        # Создание фейковых данных о погоде
        fake_data = pd.DataFrame({
            'tavg': [8.1, 7.5, 10.2, 13.0, 10.9, 5.9, 3.4, 0.8, 3.2, 2.7]
        }, index=pd.date_range(start=start_date, periods=10))

        # Создание экземпляра класса
        weather_data = WeatherData(location, start_date, end_date)

        # Вызов метода
        result = weather_data.get_weather_data()

        # Проверка результатов
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 10)
        self.assertTrue((result['tavg'] == fake_data['tavg']).all())


    @patch('meteostat.Daily')
    @patch('logging.error')
    def test_get_weather_data_failure(self, mock_logging_error, mock_daily):
        # Настройка
        location = (40.7128, -740.0060)
        start_date = '2023-01-01'
        end_date = '2023-01-10'

        # Создание экземпляра класса
        weather_data = WeatherData(location, start_date, end_date)

        # Вызов метода
        result = weather_data.get_weather_data()

        # Проверка результатов
        self.assertTrue(result.empty)






