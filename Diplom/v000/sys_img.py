import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import os


class sys_img:
    font = None
    img  = None
    draw = None
    __title_bottom = 0
    __bodies_coordinats = {}
    __system_name = ""

    def __init__(self):
        self.font_title = ImageFont.truetype("imgs\\GOTHIC.TTF", 130)
        self.font = ImageFont.truetype("imgs\\GOTHIC.TTF", 25)
        self.font_small = ImageFont.truetype("imgs\\GOTHIC.TTF", 14)
        self.img  = Image.open("imgs\\system_background_002.png")
        self.draw = ImageDraw.Draw(self.img)


    def create_title(self, in_system_name):
        """Рисуем название системы, вверху по центру"""
        img_width = self.img.width
        text_with = self.draw.textsize(in_system_name['SYSTEM_NAME'], self.font_title)[0]
        self.__title_bottom = self.draw.textsize(in_system_name['SYSTEM_NAME'], self.font_title)[1]
        #print(str(img_width)+";"+str(text_with))
        x = (img_width - text_with) / 2
        self.draw.text((x, 0), in_system_name['SYSTEM_NAME'], (255, 255, 0), font=self.font_title)
        self.__system_name = in_system_name['SYSTEM_NAME']


    def create_galaxy_map(self, in_x, in_z, in_system_name):
        """Рисуем название системы, вверху по центру"""
        img_width = self.img.width
        #text_with = self.draw.textsize(in_system_name['SYSTEM_NAME'], self.font_title)[0]
        #self.__title_bottom = self.draw.textsize(in_system_name['SYSTEM_NAME'], self.font_title)[1]
        #print(str(img_width)+";"+str(text_with))
        #x = (img_width - text_with) / 2
        #self.draw.text((x, 0), in_system_name['SYSTEM_NAME'], (255, 255, 0), font=self.font_title)

        galaxy_file = "imgs\\galaxyBackground_400.png"
        if (not os.path.isfile(galaxy_file)):
            galaxy_file = "imgs\\Unknown_Body.png"
        img_galaxy = Image.open(galaxy_file)
        #img_galaxy = img_galaxy.resize((round(body_size), round(body_size)))
        galaxy_left = self.img.width - img_galaxy.width
        galaxy_top  = self.img.height - img_galaxy.height
        self.img.paste(img_galaxy, (round(galaxy_left), round(galaxy_top)), None)

            # дорисовываем солнечную систему
        galaxy_file = "imgs\\galaxyBackground_sol_400.png"
        if (not os.path.isfile(galaxy_file)):
            galaxy_file = "imgs\\Unknown_Body.png"
        img_galaxy = Image.open(galaxy_file)
        #img_galaxy = img_galaxy.resize((round(body_size), round(body_size)))
        galaxy_left = self.img.width - img_galaxy.width
        galaxy_top  = self.img.height - img_galaxy.height
        self.img.paste(img_galaxy, (round(galaxy_left), round(galaxy_top)), img_galaxy)

            # дорисовываем систему колонии
        galaxy_file = "imgs\\galaxyBackground_colonia_400.png"
        if (not os.path.isfile(galaxy_file)):
            galaxy_file = "imgs\\Unknown_Body.png"
        img_galaxy = Image.open(galaxy_file)
        #img_galaxy = img_galaxy.resize((round(body_size), round(body_size)))
        galaxy_left = self.img.width - img_galaxy.width
        galaxy_top  = self.img.height - img_galaxy.height
        self.img.paste(img_galaxy, (round(galaxy_left), round(galaxy_top)), img_galaxy)

            # солнечная система: 197 х 308 (0 х 0 x 0)
            # Колония: 157 х 222 (-9530 x -910 x 19830)
        text_x = round( (in_x / 235) + 197)
        text_y = round(-(in_z / 235) + 308)
        print('text_x='+str(text_x)+'; text_y='+str(text_y))
        text_x = self.img.width - (img_galaxy.width-text_x)
        print('text_x='+str(text_x)+'; text_y='+str(text_y))
        text_y = text_y + (self.img.height - img_galaxy.height)
        #self.draw.text((text_x, text_y), in_system_name, (255, 255, 0), font=self.font)
            # дорисовываем точку нашей системы
        galaxy_file = "imgs\\star_point.png"
        if (not os.path.isfile(galaxy_file)):
            galaxy_file = "imgs\\Unknown_Body.png"
        img_galaxy = Image.open(galaxy_file)
        self.img.paste(img_galaxy, (text_x, text_y), img_galaxy)

    def fill_main_bodys(self, in_bodys_info):
        """Отображение солнц в главной части схемы"""
        sol_radius = 100
            # рассчитаем допустимую высоту карты системы
        max_height_img = self.img.height - self.__title_bottom
        bodies_count = len(in_bodys_info)
            # рассчитаем максимальную удалённость базовых объектов
        max_distance = (in_bodys_info[bodies_count-1]['DISTANCE_TO_ARRIVAL'] or 0) + (sol_radius * (in_bodys_info[bodies_count-1]['SOLAR_RADIUS'] or 1))
        #print('max_height_img = '+str(max_height_img))
        #print('max_distance = '+str(max_distance))

        #print(in_bodys_info)
        #print(len(in_bodys_info))

            # посчитаем максимальный размер тел в массиве
        max_body_size = 0
        for i, body in in_bodys_info.items():
            if((body['SOLAR_RADIUS'] or 1) > max_body_size):
                max_body_size = (body['SOLAR_RADIUS'] or 1)
            # пересчитаем радиус тела в пиксели
        max_body_size = round(sol_radius + (100 * max_body_size))
        if (max_body_size > 300): max_body_size = 300

        for i, body in in_bodys_info.items():
            print(body)
                # размер тела
            body_size = sol_radius + (100 * (body['SOLAR_RADIUS'] or 1))
            if(body_size > 300): body_size = 300
                # позиция х = середине самого большого тела
            body_x = 20 + (max_body_size - body_size) / 2
                # позиция у = пропорционально сверху вниз по карте системы
            body_y = (max_height_img-40) / bodies_count * i

                # определим файл тела и положим его на карту
            star_file = "imgs\\Unknown_Body.png"
            if(body['GROUP_NAME']=='Star'):
                star_file = "imgs\\stars\\" + str(body['SPECTRAL_CLASS']) + ".png"
            elif (body['GROUP_NAME'] == 'Compact star'):
                star_file = "imgs\\stars\\Neutron.png"
            elif(body['GROUP_NAME']=='Belt'):
                star_file = "imgs\\Belt.png"
            #print(star_file)
            if(not os.path.isfile(star_file)):
                star_file = "imgs\\Unknown_Body.png"
            img_star = Image.open(star_file)
            img_star = img_star.resize((round(body_size), round(body_size)))
            self.img.paste(img_star, (round(body_x), round(body_y+self.__title_bottom)), img_star)
            self.__bodies_coordinats[i] = {'x': round(body_x), 'y': round(body_y+self.__title_bottom), 'width': round(body_size), 'height': round(body_size)}

                # добавим подпись с названием
            text_msg = (body['NAME'] or "Невідомо")
            text_width = self.draw.textsize(text_msg, self.font)[0]
            text_name_height = self.draw.textsize(text_msg, self.font)[1]
            text_x = round(20 + (max_body_size - text_width)/2)
            text_y = round(body_y+self.__title_bottom + body_size)
            if(text_x < 20): text_x = 20
            self.draw.text((text_x, text_y), text_msg, (255, 255, 0), font=self.font)

                # добавим подпись с расстоянием (только если не главная звезда)
            if(not body['IS_MAIN_STAR'] == 'T'):
                #text_msg = "Відстань "+"{:,}".format((body['DISTANCE_TO_ARRIVAL'] or 0))
                text_msg = "{:,}".format((body['DISTANCE_TO_ARRIVAL'] or 0))+" ls"
                text_height = self.draw.textsize(text_msg, self.font_small)[1]
                text_width = self.draw.textsize(text_msg, self.font_small)[0]
                text_x = round(20 + (max_body_size - text_width)/2)
                text_y = round(body_y+self.__title_bottom + body_size + text_name_height)
                if(text_x < 20): text_x = 20
                self.draw.text((text_x, text_y), text_msg, (255, 255, 0), font=self.font_small)
        print(self.__bodies_coordinats)

    def fill_level_1(self, in_parent_num, in_bodies):
        """Рисуем первую линию напротив солнца"""
        #print(in_bodies)
        bodies_count = len(in_bodies)
        if(bodies_count == 0):
            return
        print(str(bodies_count))
            # рассчитаем допустимую ширину карты системы
        print(self.__bodies_coordinats[in_parent_num])
        left_edge = self.__bodies_coordinats[in_parent_num]['x'] + self.__bodies_coordinats[in_parent_num]['width'] + 70
        max_width_img = self.img.width - left_edge - 200
        print('max_width_img='+str(max_width_img)+'; left_edge='+str(left_edge))

        for i, body in in_bodies.items():
            print(body)
                # позиция х = пропорционально слева на право по карте
            body_x = ((max_width_img) / bodies_count * i) + left_edge
                # позиция x = по центру солнца
            body_y = self.__bodies_coordinats[in_parent_num]['y'] + (self.__bodies_coordinats[in_parent_num]['height']/2)
            #print('body_x='+str(body_x))

            """star_file = "imgs\\planets\\background.png"
            img_star = Image.open(star_file)
            img_star = img_star.resize((round(60), round(60)))
            self.img.paste(img_star, (round(body_x-5), round(body_y-5)), img_star)"""
            # определим файл тела и положим его на карту
            if(body['GROUP_NAME']=='Star'):
                star_file = "imgs\\stars\\" + str(body['SPECTRAL_CLASS']) + ".png"
            elif (body['GROUP_NAME'] == 'Compact star'):
                star_file = "imgs\\stars\\Neutron.png"
            elif(body['GROUP_NAME']=='Belt'):
                star_file = "imgs\\Belt.png"
            elif(body['GROUP_NAME']=='Planet'):
                star_file = "imgs\\planets\\"+str(body['TYPE_ID'])+".png"
            #print(star_file)
            if(not os.path.isfile(star_file)):
                star_file = "imgs\\Unknown_Body.png"
            star_size = (body['RADIUS'] or 1)
            star_size = round(star_size / 100)
            if(star_size > 200):
                star_size = 200
            if(star_size < 50):
                star_size = 50
            #print('star_size='+str(star_size))
            img_star = Image.open(star_file)
            if(body['GROUP_NAME']=='Belt'):
                star_size = img_star.height
            else:
                img_star = img_star.resize((round(star_size), round(star_size)))
            self.img.paste(img_star, (round(body_x), round(body_y - star_size/2)), img_star)
            if(body['IS_LANDABLE'] == 'T'):
                star_file = "imgs\\horizons.png"
                img_star = Image.open(star_file)
                img_star = img_star.resize((round(star_size), round(star_size)))
                self.img.paste(img_star, (round(body_x), round(body_y - star_size / 2)), img_star)
                ico_x = 0
                ico_y = 0
                if (body['STATION_TYPE_ID']):
                     star_file = "imgs\\ports\\"+str(body['STATION_TYPE_ID'])+".png"
                     if (os.path.isfile(star_file)):
                         img_star = Image.open(star_file)
                         img_star = img_star.resize((round(30), round(30)))
                         self.img.paste(img_star, (round(body_x+star_size), round(body_y-star_size / 2)), img_star)
                         ico_y = ico_y + 30
                     else:
                         print("file "+star_file+" not found!!!")
                     if(body['HAS_MARKET'] == 'T'):
                         star_file = "imgs\\system_icons\\market.png"
                         if (os.path.isfile(star_file)):
                             img_star = Image.open(star_file)
                             img_star = img_star.resize((round(30), round(30)))
                             self.img.paste(img_star, (round(body_x + star_size + ico_x), round(body_y - star_size / 2 + ico_y)), img_star)
                             ico_y = ico_y + 30
                     if(body['HAS_SHIPYARD'] == 'T'):
                         star_file = "imgs\\system_icons\\shipyard.png"
                         if (os.path.isfile(star_file)):
                             img_star = Image.open(star_file)
                             img_star = img_star.resize((round(30), round(30)))
                             self.img.paste(img_star, (round(body_x + star_size + ico_x), round(body_y - star_size / 2 + ico_y)), img_star)
                             ico_y = ico_y + 30
                     if(body['HAS_OUTFITTING'] == 'T'):
                         star_file = "imgs\\system_icons\\OUTFITTING.png"
                         if (os.path.isfile(star_file)):
                             img_star = Image.open(star_file)
                             img_star = img_star.resize((round(30), round(30)))
                             self.img.paste(img_star, (round(body_x + star_size + ico_x), round(body_y - star_size / 2 + ico_y)), img_star)
                             ico_y = ico_y + 30
                     if (body['HAS_BLACKMARKET'] == 'T'):
                         star_file = "imgs\\system_icons\\b_market.png"
                         if (os.path.isfile(star_file)):
                             img_star = Image.open(star_file)
                             img_star = img_star.resize((round(30), round(30)))
                             self.img.paste(img_star,(round(body_x + star_size + ico_x), round(body_y - star_size / 2 + ico_y)),img_star)
                             ico_y = ico_y + 30


                                 # добавим подпись с названием
            text_msg = (body['NAME'] or "Невідомо")
            text_msg = text_msg.replace(self.__system_name+' ', "")
            text_name_width  = self.draw.textsize(text_msg, self.font)[0]
            text_name_height = self.draw.textsize(text_msg, self.font)[1]
            #txt_img = Image.new('L', (round(text_width), round(text_width)))
            #txt_draw = ImageDraw.Draw(txt_img)
            #txt_draw.text((0, 0), text_msg, font=self.font, fill=255)
            #txt_img = txt_img.rotate(-90)
            #text_x = round(body_x) - (text_width-text_name_height) + 70
            #text_y = round(body_y)
            text_x = round(body_x + (img_star.width/2) - (text_name_width/2))
            text_y = round(body_y +  img_star.height/2)
            if(text_x < 20): text_x = 20
            self.draw.text((text_x, text_y), text_msg, (255, 255, 0), font=self.font)
            #self.img.paste(txt_img, (text_x, text_y), txt_img)

                # добавим подпись с расстоянием (только если не главная звезда)
            text_msg = "{:,}".format((body['DISTANCE_TO_ARRIVAL'] or 0))+" ls"
            text_height = self.draw.textsize(text_msg, self.font_small)[1]
            text_width = self.draw.textsize(text_msg, self.font_small)[0]
            text_x = round(text_x + text_name_width/2 - text_width/2)
            text_y = round(text_y + text_name_height)
            if(text_x < 20): text_x = 20
            self.draw.text((text_x, text_y), text_msg, (255, 255, 0), font=self.font_small)

    def fill_level_2(self, in_parent_num, in_bodies):
        """Рисуем первую линию напротив солнца"""
        print(in_bodies)

    def save(self, in_file_name):
        """Сохраняем изображение в файле"""

            # дорисовываем водяной знак сообщества
        galaxy_file = "imgs\\LogoMetalTransparent_200.png"
        if (not os.path.isfile(galaxy_file)):
            galaxy_file = "imgs\\Unknown_Body.png"
        img_galaxy = Image.open(galaxy_file)
        file_x = self.img.width - img_galaxy.width
        file_y = 0#self.img.height - img_galaxy.height
        self.img.paste(img_galaxy, (file_x, file_y), img_galaxy)

        self.img.save(in_file_name)