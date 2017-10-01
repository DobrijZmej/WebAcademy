import BaseClases
from urllib import request
import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class System(Base):
    __tablename__ = 'systems'

    id = Column(Integer, primary_key=True)
    EDSM_ID = Column(Integer)
    NAME = Column(String)


class ImportSystems(BaseClases.BaseCsv):
    def file_download(self):
        temp_file_name = os.path.join('temp', self.file_url.split('/')[-1])
        self.temp_file_name = temp_file_name
        print(f'Start downloading from [{self.file_url}] to [{temp_file_name}]')
        url_size = request.urlopen(self.file_url).info()["Content-Length"]
        print(f'File size on link: {url_size}')
        file_size = 0
        if os.path.isfile(temp_file_name):
            file_size = os.stat(temp_file_name).st_size
        print(f'File size on temp directory: {file_size}')
        self.is_need_process = True
        self.file_size = int(file_size)
        self.completed_size = 0
        if int(file_size) != int(url_size):
            request.urlretrieve(self.file_url, temp_file_name)
            print('Download complete')
        else:
            print('Download cancelled')
            self.is_need_process = False

    def read_headers(self, in_line):
        self.headers = in_line.split(',')

    def read_line(self):
        if not self.file_handler:
            self.file_handler = open(self.temp_file_name)
        return self.file_handler.readline()

    def parse_line_csv(self, in_line):
        #print(in_line)
        #print(in_line.split(','))
        line_data = in_line.split(',')
        result = {}
        for i, key in enumerate(self.headers):
            result[key] = line_data[i]
        return result

    def put_to_db(self, in_dict):
        system = System(
            id=in_dict['id'],
            EDSM_ID=in_dict['edsm_id'],
            NAME=in_dict['name'].strip('"'),
        )
        Base.metadata.create_all(self.db)
        self.session.merge(system)
        self.session.commit()

    def show_progress(self, in_line_size):
        #if self.completed_size != 0:
        #    print('\r', end='', flush=True)
        self.completed_size += in_line_size
        progress = round(self.completed_size / self.file_size * 100, 6)
        print(f'loaded {progress}%\r', end='', flush=True)





if __name__ == '__main__':
    iss = ImportSystems('https://eddb.io/archive/v5/systems.csv')
    #iss.execute('select 1')
    iss.file_download()
    if not iss.is_need_process:
        headers = iss.read_line().strip()
        iss.read_headers(headers)
        while True:
            line = iss.read_line()
            if(line == ''):
                break
            iss.show_progress(len(line))
            line = line.strip()
            #print(line)
            system_dict = iss.parse_line_csv(line)
            iss.put_to_db(system_dict)
            #print(iss.read_line())
