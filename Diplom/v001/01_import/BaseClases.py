import sqlalchemy
from sqlalchemy.orm import Session
import os
import json


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
        if os.path.isfile('config.json'):
            with open('config.json') as f_config:
                self.config = json.load(f_config)
        self.db = sqlalchemy.create_engine(
            f'postgresql://'
            f'{self.config["user"]}:'
            f'{self.config["password"]}@'
            f'{self.config["server"]}/'
            f'{self.config["database"]}')
        self.session = Session(bind=self.db)
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
