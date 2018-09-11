import logging
import sys
import pandas as pd
from scrappers.scrapper import Scrapper
from parsers.parser import Parser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
SCRAPPED_FILE = 'cian_scrapped_data.txt'
PAGES = 1


def gather_process():
    """ Собирает данные из источника и сохраняет """
    logger.info("gather")
    scrapper = Scrapper()
    scrapper.scrap_process(PAGES)


def convert_data_to_table_format():
    """ Преобразует данные из собранного вида в табличный вид """
    logger.info("transform")
    parser = Parser()
    parser.parse_data()


def stats_of_data():
    """ Подсчитывает статистики в данных """
    logger.info("stats")
    data = pd.read_csv('./data/data.csv', sep='\t')
    all_notes_count = len(data)
    one_rooms_appartments_count = len(data[data['Планировка'] == '1-комн. кв.'])
    one_rooms_appar_average_price = round(
        sum(data['Цена, руб.'][data['Планировка'] == '1-комн. кв.']) / one_rooms_appartments_count, 2)
    two_rooms_appartments_count = len(data[data['Планировка'] == '2-комн. кв.'])
    two_rooms_appar_average_price = round(sum(
        data['Цена, руб.'][data['Планировка'] == '2-комн. кв.']) / two_rooms_appartments_count, 2)
    three_rooms_appartments_count = len(data[data['Планировка'] == '3-комн. кв.'])
    three_rooms_appar_average_price = round(sum(
        data['Цена, руб.'][data['Планировка'] == '3-комн. кв.']) / three_rooms_appartments_count, 2)
    four_and_more_rooms_appartments_count = len(data[(data['Планировка'] == '4-комн. кв.') | (
        data['Планировка'] == '5-комн. кв.') | (data['Планировка'] == '6-комн. кв.')])
    free_rooms_appartments_count = len(data[data['Планировка'] == 'Своб. планировка'])
    average_m2_price = round(sum(data['Цена, руб.']) / sum(data['Площадь, м2']), 2)
    biggest_apartment = data[['Планировка', 'Площадь, м2', 'Цена, руб.']][
        data['Площадь, м2'] == data['Площадь, м2'].max()]

    print('Данные из раздела продажа квартир по г.Москва c портала cian.ru')
    print('Общее количество записей в данных: {}\n'.format(all_notes_count))
    print('Количество записей с 1-комн. квартирами: {}'.format(one_rooms_appartments_count))
    print('Количество записей с 2-комн. квартирами: {}'.format(two_rooms_appartments_count))
    print('Количество записей с 3-комн. квартирами: {}'.format(three_rooms_appartments_count))
    print('Количество записей с 4 - 6-комн. квартирами: {}'.format(four_and_more_rooms_appartments_count))
    print('Количество записей с квартирами своб. планировки: {}\n'.format(free_rooms_appartments_count))
    print('Средняя стоимость 1-комн. квартиры, руб.: {}'.format(one_rooms_appar_average_price))
    print('Средняя стоимость 2-комн. квартиры, руб.: {}'.format(two_rooms_appar_average_price))
    print('Средняя стоимость 3-комн. квартиры, руб.: {}\n'.format(three_rooms_appar_average_price))
    print('Средняя стоимость 1 м2, руб.: {}\n'.format(average_m2_price))
    print('Самая большая квартира:\n {}\n'.format(biggest_apartment))


if __name__ == '__main__':
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        gather_process()

    elif sys.argv[1] == 'transform':
        convert_data_to_table_format()

    elif sys.argv[1] == 'stats':
        stats_of_data()

    logger.info("work ended")
