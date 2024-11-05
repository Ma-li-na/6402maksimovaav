import logging
from meteostat import Point, Daily
import pandas as pd
from datetime import datetime
import geocoder
from typing import Union, Tuple


class WeatherData:
  """
  Класс для получения данных о погоде.
  """

  def __init__(self, location: Union[str, Tuple[float, float]], start_date: str, end_date: str):
    """
    Аргументы:
    location: Название города (если бы работал API ключ:) ) или координаты (широта, долгота).
    start_date: Начальная дата в формате 'YYYY-MM-DD'.
    end_date: Конечная дата в формате 'YYYY-MM-DD'.

    """
    if isinstance(location, str):
         #Получаем координаты по названию города
        location = geocoder.google(location)

    self.location = Point(location[0], location[1])
    self.start_d = datetime.strptime(start_date, '%Y-%m-%d')
    self.end_d = datetime.strptime(end_date, '%Y-%m-%d')
    self.__logger = logging.getLogger(__name__)

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

      self.__logger.info("Сервис запустился")
      return weather_data

    except Exception as e:
      self.__logger.warning("Error for get data: {e}")
      print(f"Error for get data: {e}")
      return None
