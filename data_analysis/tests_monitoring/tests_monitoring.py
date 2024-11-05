import unittest
import threading
import time
import logging
from unittest.mock import patch, MagicMock
from datetime import datetime
import numpy as np
import pandas as pd
from getdata import WeatherData 
from monitoring import DataMonitor 


class DataMonitorTest(unittest.TestCase):

  def test_init(self):
    location = np.array([55.75, 37.62]) # Пример координат
    start_date = datetime(2023, 3, 1).strftime('%Y-%m-%d')
    end_date = datetime(2023, 3, 10).strftime('%Y-%m-%d')
    interval = 30

    monitor = DataMonitor(location, start_date, end_date, interval)

    self.assertTrue(np.array_equal(monitor.location, location))
    self.assertEqual(monitor.interval, interval)
    self.assertEqual(monitor.start_d, start_date)
    self.assertEqual(monitor.end_d, end_date)
    self.assertTrue(monitor.running)

  

  @patch('time.sleep')
  @patch('getdata.WeatherData.get_weather_data')
  @patch('logging.error')
  def test_run_error(self, mock_error, mock_get_weather_data, mock_sleep):
    location = np.array([55.75, 37.62])
    start_date = datetime(2023, 3, 1).strftime('%Y-%m-%d')
    end_date = datetime(2023, 3, 10).strftime('%Y-%m-%d')

    mock_get_weather_data.side_effect = Exception("Error!") # get_weather_data должен вернуть ошибку

    monitor = DataMonitor(location, start_date, end_date)
    monitor.run()

    mock_get_weather_data.assert_called_once() #проверка, что get_weather_data вызван только один раз
    mock_error.assert_called_once() #проверка, что logging error вызван только один раз
    self.assertFalse(monitor.running)


  def test_stop(self):
    monitor = DataMonitor(np.array([0, 0]), '2023-03-01', '2023-03-10')
    monitor.running = True
    monitor.stop()
    self.assertFalse(monitor.running)

  @patch('logging.info')
  def test_stop_logging(self, mock_info):
    monitor = DataMonitor(np.array([0, 0]), '2023-03-01', '2023-03-10')
    monitor.stop()
    mock_info.assert_called_once() # проверяется, что функция logging.info была вызвана только один раз



