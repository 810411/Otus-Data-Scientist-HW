import logging
from bs4 import BeautifulSoup
import os
import csv

logger = logging.getLogger(__name__)


class Parser:
    """ Класс объекта считывающего и выбирающего данные из файла, преобразующего в табличный формат сохраненный в csv"""
    def parse_data(self):
        """ Открывает файлы с данными из папки data, парсит данные с помощью методов BeautifulSoup из html тегов
        и сохраняет в табличном виде в файл формата csv с разделением табуляцией"""
        name = './data/data.csv'
        f = open(name, 'w', encoding='UTF-8')
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(
            ['Метро', 'Адрес', 'Планировка', 'Площадь, м2', 'Этаж', 'Этажность здания', 'Цена, руб.', 'Описание'])
        for filename in os.listdir('data'):
            with open('./data/{}'.format(filename), 'rb') as fl:
                page = fl.read().decode()
            soup = BeautifulSoup(page, 'lxml')
            cian_ads = soup.find_all(class_='_93444fe79c-card--2Jgih')
            for ad in cian_ads:
                title = self._try_to_get_content(ad, 'c6e8ba5398-title--3WDDX').split(',')
                rooms = title[0]
                square = self._convert_to_int(title[1].split()[0])
                floors = title[2].split('/')
                floor = self._convert_to_int(floors[0])
                floors = self._convert_to_int(floors[1])
                price = self._convert_to_int(self._try_to_get_content(ad, 'c6e8ba5398-header--6WXYW'))
                metro = self._try_to_get_content(ad, 'c6e8ba5398-underground-name--2L8eg')
                address = self._take_from_attribute_content(
                    self._try_to_get_content(ad, 'c6e8ba5398-address-links--1I9u5'))
                desc = self._try_to_get_content(ad,
                                                'c6e8ba5398-container--_4ZtZ c6e8ba5398-info-section--28o47').replace(
                    '\n', ' ')
                writer.writerow([metro, address, rooms, square, floor, floors, price, desc])
        f.close()
        logger.info('{} saved'.format(name))

    def _try_to_get_content(self, page, class__):
        content = ''
        try:
            content = str(page.find(class_=class__).contents[0]).strip()
            return content
        except AttributeError:
            return content

    def _take_from_attribute_content(self, tag):
        tag = tag.partition('content=')[2].split('"')[1]
        return tag

    def _convert_to_int(self, string_):
        try:
            return int(''.join([_ for _ in string_ if _.isdigit()]))
        except ValueError:
            return None
