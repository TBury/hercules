import requests
import json

from django.conf import settings
from celery import shared_task
from . import recognition


@shared_task
def get_waybill_info(first_screen_path, second_screen_path):
    ocr = recognition.WaybillInfo(
        first_screen.path,
        end_screen.path)
    waybill = {
        'loading_city': ocr.loading_city,
        'loading_spedition': ocr.loading_spedition,
        'unloading_city': ocr.unloading_city,
        'unloading_spedition': ocr.unloading_spedition,
        'distance': ocr.distance,
        'fuel': ocr.fuel,
        'cargo': ocr.cargo,
        'tonnage': ocr.tonnage,
        'income': ocr.income,
    }
    waybill = json.dumps(waybill, indent=4)
    return waybill
