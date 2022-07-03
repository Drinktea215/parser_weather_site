from os import remove
from model import DatabaseUpdater
from datetime import datetime, timedelta
from imagemaker import ImageMaker
from weathermaker import WeatherMaker


class Manager:
    def __init__(self):
        self.forecast = []

    def start(self, city):
        url = f'https://yandex.ru/pogoda/{city}/details?via=ms'
        weather_forecast = WeatherMaker(url)
        self.forecast = weather_forecast.go()

    def date_process(self):
        print('Введите диапазон дат (в формате dd.mm-dd.mm):')
        data = input().replace(' ', '')
        start_date = datetime.strptime(data.split('-')[0], '%d.%m')
        end_date = datetime.strptime(data.split('-')[1], '%d.%m')
        start_date = datetime.date(start_date)
        end_date = datetime.date(end_date)
        return start_date, end_date

    def receive_request(self):
        print('Сервис Яндекс.Погода любезно предоставил нам прогноз погоды на ближайшие 10 дней. Что хотите сделать?\n'
              '1. Подготовить открытки за указанный диапазон дат.\n'
              '2. Внести в базу данных прогноз погоды за указанный диапазон дат.\n'
              '3. Получить из базы данных прогноз погоды за указанный диапазон дат.\n'
              '4. Удалить базу данных.\n'
              '5. Не удалять базу данных.\n'
              '6. Выйти.')
        what_shall_we_do = input()
        return what_shall_we_do

    def go(self):
        while True:
            what_shall_we_do = self.receive_request()
            if what_shall_we_do in ['1', '2', '3']:
                start_date, end_date = self.date_process()
                while start_date <= end_date:
                    for one_day in self.forecast:
                        if one_day['date'] == start_date:
                            if what_shall_we_do == '1':
                                maker = ImageMaker(one_day, 'python_snippets/external_data/probe.jpg')
                                maker.go()
                                break
                            elif what_shall_we_do == '2':
                                dbup = DatabaseUpdater(one_day)
                                dbup.update()
                            else:
                                dbup = DatabaseUpdater([start_date, end_date])
                                data = dbup.get_get()
                                for day in data:
                                    print(day['date'], day['forecast'], day['temperature'])
                            break
                    if what_shall_we_do == '3':
                        break
                    start_date += timedelta(days=1)
                print('Готово!')
            elif what_shall_we_do == '4':
                try:
                    remove('Weather.db')
                    print('Готово!')
                except Exception:
                    print('Что-то пошло не так. :(')
            elif what_shall_we_do == '5':
                print('Это было легко! :)')
            elif what_shall_we_do == '6':
                break
            else:
                print('Боюсь я вас не понял. Попробуйте еще раз.')
