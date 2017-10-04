import BaseClases
from urllib import request
import os
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

import csv


class System(Base):
    __tablename__ = 'systems'

    id = Column(Integer, primary_key=True)
    EDSM_ID = Column(Integer)
    NAME = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    POPULATION = Column(Integer)
    IS_POPULATED = Column(Boolean)
    GOVERNMENT_ID = Column(Integer)
    ALLEGIANCE_ID = Column(Integer)
    STATE_ID = Column(Integer)
    SECURITY_ID = Column(Integer)
    PRIMARY_ECONOMY_ID = Column(Integer)
    POWER = Column(String)
    POWER_STATE_ID = Column(Integer)
    NEEDS_PERMIT = Column(Boolean)
    UPDATED_AT = Column(DateTime)
    SIMBAD_REF = Column(String)
    CONTROLLING_MIN_FACT_ID = Column(Integer)
    RESERVE_TYPE_ID = Column(Integer)
    NAME_UPPER = Column(String)



class ImportSystems(BaseClases.BaseCsv):
    def __del__(self):
        if self.file_handler:
            self.file_handler.close()

    def file_download(self):
        temp_file_name = os.path.join('temp', self.file_url.split('/')[-1])
        self.temp_file_name = temp_file_name
        print(f'Start downloading from '
              f'[{self.file_url}] to '
              f'[{temp_file_name}]')
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
            self.reader = csv.DictReader(self.file_handler)
        return next(self.reader)
        # return self.file_handler.readline()

    def parse_line_csv(self, in_line):
        # print(in_line)
        # print(in_line.split(','))
        line_data = in_line.split(',')
        result = {}
        for i, key in enumerate(self.headers):
            result[key] = line_data[i]
        return result

    def put_to_db(self, in_dict):
        system = System(
            id=int(in_dict['id']),
            EDSM_ID=int(in_dict['edsm_id']),
            NAME=in_dict['name'].strip('"'),
            x=float(in_dict['x']),
            y=float(in_dict['y']),
            z=float(in_dict['z']),
            POPULATION=int(in_dict['population']),
            IS_POPULATED=bool(in_dict['is_populated']),
            GOVERNMENT_ID=int(in_dict['government_id']),
            ALLEGIANCE_ID=int(in_dict['allegiance_id']),
            STATE_ID=int(in_dict['state_id']),
            SECURITY_ID=int(in_dict['security_id']),
            PRIMARY_ECONOMY_ID=int(in_dict['primary_economy_id']),
            POWER=in_dict['power'].strip('"'),
            POWER_STATE_ID=int(in_dict['power_state_id']),
            NEEDS_PERMIT = bool(in_dict['needs_permit']),

        UPDATED_AT = Column(DateTime)
        SIMBAD_REF = Column(String)
        CONTROLLING_MIN_FACT_ID = Column(Integer)
        RESERVE_TYPE_ID = Column(Integer)
        NAME_UPPER = Column(String)

        )
        Base.metadata.create_all(self.db)
        self.session.merge(system)
        self.session.commit()

    def show_progress(self, in_line_size):
        # if self.completed_size != 0:
        #     print('\r', end='', flush=True)
        self.completed_size += in_line_size
        progress = round(self.completed_size / self.file_size * 100, 6)
        print(f'loaded {progress}%\r', end='', flush=True)


if __name__ == '__main__':
    iss = ImportSystems('https://eddb.io/archive/v5/systems.csv')
    # iss.execute('select 1')
    iss.file_download()
    if not iss.is_need_process:
        i = 0
        line = '-'
        while line:
        #for line in iss.read_line():
            line  = iss.read_line()
            # print(line)
            iss.put_to_db(line)
            print(f'{i} lines imported...', end='\r')
            i += 1



        # headers = iss.read_line().strip()
        # iss.read_headers(headers)
        # while True:
        #     line = iss.read_line()
            # print(line)
            # if not line:
            #     break
            # iss.show_progress(len(line))
            # line = line.strip()
            # # print(line)
            # system_dict = iss.parse_line_csv(line)
            # iss.put_to_db(line)
            # # print(iss.read_line())
