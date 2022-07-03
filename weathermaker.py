import requests
import bs4
from datetime import datetime

month_global = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
                'ноября', 'декабря']


class WeatherMaker:
    def __init__(self, weather_url):
        self.weather_url = weather_url
        self.forecast = []

    def go(self):
        html = requests.get(self.weather_url).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        block = soup.find_all('div', {'class': 'card'})
        # block.pop(1)  # Реклама
        # block.pop(-1)  # Реклама
        for day in block:
            date = day.find_all('strong', {'class': 'forecast-details__day-number'})
            month = day.find_all('span', {'class': 'forecast-details__day-month'})
            weather = day.find_all('td', {'class': 'weather-table__body-cell weather-table__body-cell_type_condition'})
            temperatures = day.find_all('td',
                                        {'class': 'weather-table__body-cell weather-table__body-cell_type_feels-like'})
            temper = temperatures[1].find_all('span', {'class': 'temp__value'})
            date_2 = f'{date[0].text}.{month_global.index(month[0].text) + 1}'
            date_2 = datetime.strptime(date_2, '%d.%m')
            date_2 = datetime.date(date_2)
            one_day = {
                'forecast': weather[1].text,
                'temperature': temper[0].text + '°',
                'date': date_2}
            self.forecast.append(one_day)
        return self.forecast
