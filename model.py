from peewee import *

db = SqliteDatabase('Weather.db')


class WeatherForecast(Model):
    date = DateField(unique=True)
    forecast = CharField()
    temperature = CharField()

    class Meta:
        database = db


class DatabaseUpdater:
    def __init__(self, one_day):
        self.one_day = one_day

    def update(self):
        weather, created = WeatherForecast.get_or_create(date=self.one_day['date'],
                                                         defaults={'forecast': self.one_day['forecast'],
                                                                   'temperature': self.one_day['temperature']})
        if not created:
            query = weather.update(forecast=self.one_day['forecast'],
                                   temperature=self.one_day['temperature']
                                   ).where(WeatherForecast.date == weather.date)
            query.execute()

    def get_get(self):
        data = []
        for day in WeatherForecast.select().where(WeatherForecast.date.between(self.one_day[0], self.one_day[1])):
            data.append({'date': day.date, 'forecast': day.forecast, 'temperature': day.temperature})
        return data


db.create_tables([WeatherForecast])
