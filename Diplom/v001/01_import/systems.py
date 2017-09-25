import psycopg2

class ImportSystems:
    def __init__(self):
        self.connect = psycopg2.connect(dbname='eddb', user='ueddb', password='7014258')

    def get_file(self):
        """
        Загрузка файла по ссылке https://eddb.io/archive/v5/systems.csv
        :return: 
        """
        pass

    def file_read_line(self):
        """
        Вычитка следующей строки файла, анализ и запись в БД
        :return: 
        """

    def execute(self, in_sql):
        cur = self.connect.cursor()
        cur.execute(in_sql)

if __name__ == '__main__':
    iss = ImportSystems()
    iss.execute('select 1')