import requests

from django.conf import settings
from celery import shared_task
from . import recognition


@shared_task
def get_loading_city(ocr):
    loading_city = ocr.get_loading_city()
    return loading_city

@shared_task
def get_loading_spedition(ocr):
    loading_spedition = ocr.get_loading_spedition()
    return loading_spedition

@shared_task
def get_unloading_city(ocr):
    unloading_city = ocr.get_unloading_city()
    return unloading_city

@shared_task
def get_unloading_spedition(ocr):
    unloading_spedition = ocr.get_unloading_spedition()
    return unloading_spedition

@shared_task
def get_cargo(ocr):
    cargo = ocr.get_cargo()
    return cargo

@shared_task
def get_tonnage(ocr):
    tonnage = ocr.get_tonnage()
    return tonnage

@shared_task
def get_distance(ocr):
    distance = ocr.get_distance()
    return distance

@shared_task
def get_fuel(ocr):
    fuel = ocr.get_fuel()
    return fuel

@shared_task
def get_income(ocr):
    income = ocr.get_income()
    return income

@shared_task
def get_waybill_info(first_screen_path, end_screen_path):
    ocr = recognition.WaybillInfo(
        first_screen_path,
        end_screen_path)
    loading_city = get_loading_city(ocr)
    loading_spedition = get_loading_spedition(ocr)
    unloading_city = get_unloading_city(ocr)
    unloading_spedition = get_unloading_spedition(ocr)
    cargo = get_cargo(ocr)
    tonnage = get_tonnage(ocr)
    distance = get_distance(ocr)
    fuel = get_fuel(ocr)
    income = get_income(ocr)
    waybill = {
        'loading_city': loading_city,
        'loading_spedition': loading_spedition,
        'unloading_city': unloading_city,
        'unloading_spedition': unloading_spedition,
        'cargo': cargo,
        'tonnage': tonnage,
        'distance': distance,
        'fuel': fuel,
        'income': income,
    }
    return waybill
