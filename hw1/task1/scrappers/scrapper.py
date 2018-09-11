import logging
import time
import requests

logger = logging.getLogger(__name__)


class Scrapper():
    """ Класс объекта для сбора данных с сайта """

    def scrap_process(self, pages=1, filename='cian_page'):
        """ Получаем и сохраняем страницы сайта cian.ru из раздела продажи квартир в г.Москва """
        for p in range(1, pages + 1):
            url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={}&region=1'.format(p)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/68.0.3440.106 Safari/537.36'}
            response = requests.get(url, headers=headers)
            if not response.ok:
                logger.error(response.text)
            else:
                data = response.text
                name = './data/{}_{}.bin'.format(filename, p)
                try:
                    with open(name, 'wb') as fl:
                        fl.write(data.encode())
                        logger.info('{} saved'.format(name))
                except Exception as e:
                    logger.info(e)
            time.sleep(5)
