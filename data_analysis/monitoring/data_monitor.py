import threading
import time
import logging
from meteostat import Point, Daily
from datetime import datetime
import numpy as np 
from getdata import WeatherData


class DataMonitor(threading.Thread):
    def __init__(self, location: np.ndarray, start_date: str, end_date: str, interval: int = 60):
        """
        Инициализация класса DataMonitor.

        Args:
        location: Объект Point, представляющий местоположение, для которого будет производиться мониторинг.
        interval: Интервал в секундах, с которым будет выполняться проверка новых данных (по умолчанию 60 секунд).
        """
        super().__init__() # Вызов метода инициализации родительского класса
        self.location = location
        self.interval = interval
        self.start_d = start_date
        self.end_d = end_date
        self.__logger = logging.getLogger(__name__)
        self.running = True

    def run(self):
        """
        Запускает цикл мониторинга данных.
        """
        while self.running:
            try:
                # Получаем текущие данные о погоде
                current_data = WeatherData(self.location, self.start_d, self.end_d)
                current_data = current_data.get_weather_data()
                if current_data is not None and not current_data.empty:
                    self.__logger.info("Current data of weather: {current_data}")
                    print(f"Current data of weather: ")
                    print(f"{current_data}")
                time.sleep(self.interval)
            except Exception as e:
                self.__logger.warning("Error of theard in monitoring: {e}")
                self.running = False

    def stop(self):
        """
        Останавливает цикл мониторинга.
        """
        self.running = False
        self.__logger.info("Monitoring is stop")
        
