import logging
from meteostat import Point, Daily
import pandas as pd
from datetime import datetime
import geocoder
from typing import Union, Tuple

# Настройка логирования
logging.basicConfig(level=logging.WARNING, filename='logs/get_data.log', 
          format='%(asctime)s - %(levelname)s - %(message)s')

class WeatherData:
  """
  Класс для получения данных о погоде.
  """

  def __init__(self, location: Union[str, Tuple[float, float]], start_date: str, end_date: str):
    """
    Аргументы:
    location: Название города или координаты (широта, долгота).
    start_date: Начальная дата в формате 'YYYY-MM-DD'.
    end_date: Конечная дата в формате 'YYYY-MM-DD'.

    """
    if isinstance(location, str):
         #Получаем координаты по названию города
        location = geocoder.google(location)

    self.location = Point(location[0], location[1])
    self.start_d = datetime.strptime(start_date, '%Y-%m-%d')
    self.end_d = datetime.strptime(end_date, '%Y-%m-%d')

  def get_weather_data(self) -> pd.DataFrame:
    """
    Получение данных о погоде для заданного местоположения и периода времени.
    Аргументы:

    Возвращает:
     DataFrame с данными о погоде.
    """
    try:

      data = Daily(self.location, start=self.start_d, end=self.end_d)
      weather_data = data.fetch()
      weather_data = weather_data[['tavg']]

      logging.info(f"OK")
      return weather_data

    except Exception as e:
      logging.error(f"Error for get data: {e}")
      print(f"Error for get data: {e}")
      return None
