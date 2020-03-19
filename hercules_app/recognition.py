from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageChops
import pytesseract
import re
import os

TESSERACT_CMD = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


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
            first_screen = Image.open(self.first_screen_path)
        except KeyError:
            return "Błąd otwarcia pliku"
        return first_screen

    def get_end_screen(self):
        try:
            end_screen = Image.open(self.end_screen_path)
        except KeyError:
            return "Błąd otwarcia pliku"
        return end_screen

    def crop_screen(self, screen, x1, y1, x2, y2):
        screen = screen.crop((x1, y1, x2, y2))
        screen.filter = (ImageFilter.SHARPEN)
        return screen

    def regex_process(self, info, pattern):
        pattern_ = re.compile(pattern)
        matches = tuple(pattern_.findall(info))
        return matches[0]

    def get_loading_info(self):
        first_screen = self.crop_screen(
            self.first_screen, 1432, 608, 1800, 632)
        loading_info = pytesseract.image_to_string(first_screen, lang='pol')
        return loading_info

    def get_loading_city(self):
        loading_city = self.regex_process(self.loading_info, r'.+?(?=\()')
        loading_city = loading_city.rstrip()
        return loading_city

    def get_loading_spedition(self):
        loading_spedition = self.regex_process(
            self.loading_info, r'(?<=\/).*$')
        loading_spedition = loading_spedition.lstrip()
        return loading_spedition

    def get_unloading_info(self):
        first_screen = self.crop_screen(
            self.first_screen, 1431, 643, 1800, 663)
        unloading_info = pytesseract.image_to_string(first_screen, lang='pol')
        return unloading_info

    def get_unloading_city(self):
        unloading_city = self.regex_process(
            self.unloading_info,
            r'.+?(?=\()'
        )
        unloading_city = unloading_city.rstrip()
        return unloading_city

    def get_unloading_spedition(self):
        unloading_spedition = self.regex_process(
            self.unloading_info,
            r'(?<=\/).*$'
        )
        unloading_spedition = unloading_spedition.lstrip()
        return unloading_spedition

    def get_cargo(self):
        first_screen = self.crop_screen(
            self.first_screen, 1257, 123, 1669, 150)
        cargo = pytesseract.image_to_string(first_screen, lang='pol')
        return cargo

    def get_tonnage(self):
        first_screen = self.crop_screen(
            self.first_screen, 1431, 735, 1521, 754)
        tonnage = pytesseract.image_to_string(first_screen, lang='pol')
        return tonnage

    def get_distance(self):
        end_screen = self.crop_screen(self.end_screen, 1078, 264, 1211, 290)
        distance = pytesseract.image_to_string(end_screen, lang='pol')
        distance = distance[:-2]
        return distance

    def get_fuel(self):
        end_screen = self.crop_screen(self.end_screen, 706, 339, 1215, 370)
        fuel = pytesseract.image_to_string(end_screen, lang='pol')
        fuel = self.regex_process(fuel, r'(\d+,\d)')
        return fuel

    def get_income(self):
        end_screen = self.crop_screen(self.end_screen, 965, 792, 1202, 819)
        income = pytesseract.image_to_string(end_screen)
        income = income.replace(" ", "")
        income = self.regex_process(income, r'(\d+)')
        return income
