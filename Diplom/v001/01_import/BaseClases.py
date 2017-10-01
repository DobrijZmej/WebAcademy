import sqlalchemy
from sqlalchemy.orm import Session
import os

class BaseImport:
    """
    Базовый класс загрузки и импорта файлов
    """
    file_handler = None

    def __init__(self, in_url):
        """
        Конструктор, инициализация подключения к БД
        :param in_url: адрес к файлу, который необходимо загрузить
        """
        self.file_url = in_url
        self.db = sqlalchemy.create_engine('postgresql://ueddb:7014258@localhost/eddb')
        self.session =Session(bind=self.db)
        #self.db = psycopg2.connect(dbname='eddb', user='ueddb', password='7014258')
        if not os.path.exists('temp'):
            os.makedirs('temp')

    def file_download(self):
        """
        Загрузить файл и сохранить во временный каталог
        """
        pass


class BaseCsv(BaseImport):
    """
    Класс парсинга для файлов типа CSV
    """

    def parse_line_csv(self):
        """
        Считываем строку из файла и загружаем в ORM
        """
        pass

class BaseJson(BaseImport):
    """
    Класс парсинга для файлов типа json
    """
    def parse_line_json(self):
        """
        Считываем строку из файла и загружаем в ORM
        """
        pass
