import requests

from django.conf import settings
from celery import shared_task
from . import recognition
from django_celery_results.models import TaskResult


@shared_task
def get_loading_city(ocr, bind=True):
    loading_city = ocr.get_loading_city()
    return loading_city

@shared_task
def get_loading_spedition(ocr, bind=True):
    loading_spedition = ocr.get_loading_spedition()
    return loading_spedition

@shared_task
def get_unloading_city(ocr, bind=True):
    unloading_city = ocr.get_unloading_city()
    return unloading_city

@shared_task
def get_unloading_spedition(ocr, bind=True):
    unloading_spedition = ocr.get_unloading_spedition()
    return unloading_spedition

@shared_task
def get_cargo(ocr, bind=True):
    cargo = ocr.get_cargo()
    return cargo

@shared_task
def get_tonnage(ocr, bind=True):
    tonnage = ocr.get_tonnage()
    return tonnage

@shared_task
def get_distance(ocr, bind=True):
    distance = ocr.get_distance()
    return distance

@shared_task
def get_fuel(ocr, bind=True):
    fuel = ocr.get_fuel()
    return fuel

@shared_task
def get_income(ocr, bind=True):
    income = ocr.get_income()
    return income

@shared_task
def get_waybill_info(first_screen_path, end_screen_path, bind=True):
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
