import json
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

def get_country(city_name):
    with open('static/assets/files/companies.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        for city in data:
            if city.get("city_name") == city_name:
                return city.get("country")
                break
    return None

def file_exists(spedition):
    try:
        spedition = str(spedition).lower()
        abs_path = finders.find(f"/static/assets/companies/{ spedition }.png")
        if staticfiles_storage.exists(abs_path):
            return abs_path
        return "assets/companies/no_company.png"
    except IOError:
        return "assets/companies/no_company.png"