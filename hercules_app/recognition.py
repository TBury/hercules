import re

from PIL import Image, ImageFilter
from io import BytesIO
from django.core.files.storage import default_storage as storage
from pytesseract import image_to_string, tesseract_cmd

tesseract_cmd = '/app/.apt/usr/bin/tesseract'

class WaybillInfo:
    def __init__(self, first_screen_path, end_screen_path):
        self.first_screen_path = first_screen_path
        self.end_screen_path = end_screen_path
        self.first_screen = self.get_first_screen()
        self.end_screen = self.get_end_screen()

        self.loading_info = self.get_loading_info()
        self.unloading_info = self.get_unloading_info()

    def get_first_screen(self):
        try:
            fs = storage.open(self.first_screen_path, mode="rb")
            first_screen = Image.open(fs)
        except KeyError:
            return "Błąd otwarcia pliku"
        return first_screen

    def get_end_screen(self):
        try:
            f = storage.open(self.end_screen_path, "rb")
            end_screen = Image.open(f)
        except KeyError:
            return "Błąd otwarcia pliku"
        return end_screen

    def crop_screen(self, screen, x1, y1, x2, y2):
        screen = screen.crop((x1, y1, x2, y2))
        screen.filter = (ImageFilter.SHARPEN)
        return screen

    def resize_screen(self, screen, percent):
        screen_width = int((screen.width * percent)/100)
        screen_height = int((screen.height * percent)/100)
        screen = screen.resize(
            (screen_width, screen_height), Image.BICUBIC)
        return screen

    def regex_process(self, info, pattern):
        _pattern = re.compile(pattern)
        matches = tuple(_pattern.findall(info))
        if len(matches) > 0:
            return matches[0]
        return 'error'

    def get_loading_info_image(self):
        first_screen = self.crop_screen(
            self.first_screen, 1432, 608, 1800, 632)
        return first_screen

    def get_unloading_info_image(self):
        first_screen = self.crop_screen(
            self.first_screen, 1431, 643, 1800, 663)
        return first_screen

    def get_loading_info(self):
        first_screen = self.get_loading_info_image()
        loading_info = image_to_string(first_screen, lang='pol')
        return loading_info

    def get_loading_city(self):
        loading_city = self.regex_process(self.loading_info, r'.+?(?=\()')
        if loading_city != 'error':
            loading_city = loading_city.rstrip()
        return loading_city

    def get_loading_spedition(self):
        loading_spedition = self.regex_process(
            self.loading_info, r'(?<=\/).*$')
        if loading_spedition != 'error':
            loading_spedition = loading_spedition.lstrip()
        return loading_spedition

    def get_unloading_info(self):
        first_screen = self.get_unloading_info_image()
        unloading_info = image_to_string(first_screen, lang='pol')
        return unloading_info

    def get_unloading_city(self):
        unloading_city = self.regex_process(
            self.unloading_info,
            r'.+?(?=\()'
        )
        if unloading_city != 'error':
            unloading_city = unloading_city.rstrip()
        return unloading_city

    def get_unloading_spedition(self):
        unloading_spedition = self.regex_process(
            self.unloading_info,
            r'(?<=\/).*$'
        )
        if unloading_spedition != 'error':
            unloading_spedition = unloading_spedition.lstrip()
        return unloading_spedition

    def get_cargo_image(self):
        first_screen = self.crop_screen(
            self.first_screen, 1250, 121, 1620, 168)
        return first_screen

    def get_cargo(self):
        first_screen = self.get_cargo_image()
        cargo = image_to_string(first_screen, lang='pol')
        return cargo

    def get_tonnage_image(self):
        first_screen = self.crop_screen(
            self.first_screen, 1431, 735, 1521, 754)
        return first_screen

    def get_tonnage(self):
        first_screen = self.get_tonnage_image()
        tonnage = image_to_string(first_screen, lang='pol')
        tonnage = tonnage[:-3]
        tonnage = tonnage.replace(" ", "")
        return tonnage

    def get_distance_image(self):
        end_screen = self.crop_screen(self.end_screen, 1112, 267, 1199, 286)
        return end_screen

    def get_distance(self):
        end_screen = self.get_distance_image()
        end_screen = self.resize_screen(end_screen, 225)
        distance = image_to_string(end_screen)
        distance = self.regex_process(distance, r'(\d+)')
        return distance

    def get_fuel_image(self):
        end_screen = self.crop_screen(self.end_screen, 706, 335, 1400, 372)
        return end_screen

    def get_fuel(self):
        end_screen = self.get_fuel_image()
        end_screen = self.resize_screen(end_screen, 300)
        fuel = image_to_string(end_screen, lang='pol')
        fuel = self.regex_process(fuel, r'(\d+,\d)')
        if fuel != 'error':
            fuel = fuel.replace(',', '.')
            fuel = round(float(fuel))
        return fuel

    def get_income_image(self):
        end_screen = self.crop_screen(self.end_screen, 1090, 789, 1190, 820)
        return end_screen

    def get_income(self):
        end_screen = self.get_income_image()
        end_screen = self.resize_screen(end_screen, 275)
        income = image_to_string(end_screen, lang='pol')
        income = income.replace(" ", "")
        income = self.regex_process(income, r'(\d+)')
        return income

    def save_to_s3(self, image, image_name):
        output = BytesIO()
        image.save(output, format="JPEG")
        with storage.open(image_name, 'w+') as f:
            f.write(output.getvalue())
        output.close()

    def save_loading_info_screen(self, id):
        loading_info_screen = self.get_loading_info_image()
        file_name = 'waybills/%s' % str(id) + 'loading-info.png'
        self.save_to_s3(loading_info_screen, file_name)

    def save_unloading_info_screen(self, id):
        unloading_info_screen = self.get_unloading_info_image()
        file_name = 'waybills/%s-unloading-info.png' % str(
            id)
        self.save_to_s3(unloading_info_screen, file_name)

    def save_cargo_screen(self, id):
        cargo = self.get_cargo_image()
        file_name = 'waybills/%s-cargo.png' % str(
            id)
        self.save_to_s3(cargo, file_name)

    def save_tonnage_screen(self, id):
        tonnage = self.get_tonnage_image()
        file_name = 'waybills/%s-tonnage.png' % str(
            id)
        self.save_to_s3(tonnage, file_name)

    def save_distance_screen(self, id):
        distance = self.get_distance_image()
        file_name = 'waybills/%s-distance.png' % str(
            id)
        self.save_to_s3(distance, file_name)

    def save_fuel_screen(self, id):
        fuel = self.get_fuel_image()
        file_name = 'waybills/%s-fuel.png' % str(
            id)
        self.save_to_s3(fuel, file_name)

    def save_income_screen(self, id,):
        income = self.get_income_image()
        file_name = 'waybills/%s-income.png' % str(id)
        self.save_to_s3(income, file_name)
