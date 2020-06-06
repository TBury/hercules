import json


def get_country(city_name):
    with open('static/assets/files/companies.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        for city in data:
            if city.get("city_name") == city_name:
                return city.get("country")
                break
    return None
