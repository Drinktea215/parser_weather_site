import cv2
from random import randint, choice
from datetime import datetime
from os import mkdir, listdir
from weathermaker import month_global


class ImageMaker:
    def __init__(self, one_day, image_back='python_snippets/external_data/probe.jpg'):
        self.date = one_day['date']
        self.weather = one_day['forecast']
        self.temperature = one_day['temperature']
        self.image_back = image_back

    def go(self):
        image_back = cv2.imread(self.image_back)
        image = image_back.copy()
        file_name_with_weather, color = self.change_color()
        force = self.determine_force()

        self.grad(image, color)
        self.add_image(image, file_name_with_weather, force)
        self.add_weather(image)
        self.add_date(image)
        self.add_temperature(image)

        cv2.imshow("image", image)
        catalog_name = datetime.now().strftime('%m')
        if catalog_name not in listdir():
            mkdir(catalog_name)
        image_name = f'{catalog_name}/{self.date.split(" ")[0]}.jpg'
        cv2.imwrite(image_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def grad(self, image, color):
        x1 = None
        for x2 in range(1, image.shape[0]):
            coockes = (color['b'], color['g'], color['r'])
            image[x1:x2, :] = coockes
            x1 = x2
            color['b'] += 1 if color['b'] < 255 else 0
            color['g'] += 1 if color['g'] < 255 else 0
            color['r'] += 1 if color['r'] < 255 else 0

    def change_color(self):
        filenames = ['sun.jpg', 'rain.jpg', 'snow.jpg', 'cloud.jpg']
        if 'ясн' in self.weather.lower():
            return filenames[0], {'b': 0, 'g': 255, 'r': 255}
        elif 'дожд' in self.weather.lower():
            return filenames[1], {'b': 255, 'g': 0, 'r': 0}
        elif 'снег' in self.weather.lower():
            return filenames[2], {'b': 255, 'g': 255, 'r': 0}
        elif 'облач' in self.weather.lower() or 'пасмурн' in self.weather.lower():
            return filenames[3], {'b': 0, 'g': 0, 'r': 0}
        else:  # Для всего остального - случайная картинка и случайный градиент
            return choice(filenames), {'b': randint(0, 255), 'g': randint(0, 255), 'r': randint(0, 255)}

    def add_date(self, image):
        self.date = self.date.strftime('%d.%m')
        date = self.date.split('.')
        date[1] = month_global[int((date[1])) - 1]
        cv2.putText(image, date[0], (450, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, date[1], (400, 65), cv2.FONT_HERSHEY_COMPLEX, .6, (0, 0, 255), 1)

    def add_weather(self, image):
        if self.weather == 'Облачно с прояснениями':  # Непредвиденный вариант погоды :)
            weather = self.weather.split(' ')
            cv2.putText(image, weather[0], (30, 220), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
            cv2.putText(image, f'{weather[1]} {weather[2]}', (30, 240), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
        else:
            cv2.putText(image, self.weather, (30, 220), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    def add_image(self, image, file_name_with_weather, force=1):
        image_weather = cv2.imread(f'python_snippets/external_data/weather_img/{file_name_with_weather}')
        weather = image_weather[:, :]
        y1 = 15
        y2 = 15
        for _ in range(force):
            y2 += weather.shape[1]
            image[20:20 + weather.shape[0], y1:y2] = weather
            y1 = y2

    def determine_force(self):
        if 'сильн' in self.weather.lower() or 'пасмур' in self.weather.lower():
            return 3
        elif 'небольш' in self.weather.lower() or 'мало' in self.weather.lower():
            return 1
        elif 'ясн' in self.weather.lower() and 'обл' in self.weather.lower():
            return 1
        else:
            return 2

    def add_temperature(self, image):
        cv2.putText(image, self.temperature, (350, 220), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2)
