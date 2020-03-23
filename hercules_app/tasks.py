import requests

from django.conf import settings
from celery import shared_task
from . import recognition
from django_celery_results.models import TaskResult
import uuid


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
def save_loading_info_screen(ocr, id, bind=True):
    loading_info_screen = ocr.get_loading_info_image()
    loading_info_screen.save('hercules_app\\static\\hercules_app\\media\\%s' % str(
        id) + 'loading-info.png', 'JPEG')


@shared_task
def save_unloading_info_screen(ocr, id, bind=True):
    unloading_info_screen = ocr.get_unloading_info_image()
    unloading_info_screen.save('hercules_app\\static\\hercules_app\\media\\%s' %
                               str(id) + 'unloading-info.png', 'JPEG')


@shared_task
def save_cargo_screen(ocr, id, bind=True):
    cargo = ocr.get_cargo_image()
    cargo.save('hercules_app\\static\\hercules_app\\media\\%s' %
               str(id) + 'cargo.png', 'JPEG')


@shared_task
def save_tonnage_screen(ocr, id, bind=True):
    tonnage = ocr.get_tonnage_image()
    tonnage.save('hercules_app\\static\\hercules_app\\media\\%s' %
                 str(id) + 'tonnage.png', 'JPEG')


@shared_task
def save_distance_screen(ocr, id, bind=True):
    distance = ocr.get_distance_image()
    distance.save('hercules_app\\static\\hercules_app\\media\\%s' %
                  str(id) + 'distance.png', 'JPEG')


@shared_task
def save_fuel_screen(ocr, id, bind=True):
    fuel = ocr.get_fuel_image()
    fuel.save('hercules_app\\static\\hercules_app\\media\\%s' %
              str(id) + 'fuel.png', 'JPEG')


@shared_task
def save_income_screen(ocr, id, bind=True):
    income = ocr.get_income_image()
    income.save('hercules_app\\static\\hercules_app\\media\\%s' %
                str(id) + 'income.png', 'JPEG')


@shared_task
def get_waybill_info(first_screen_path, end_screen_path, bind=True):
    ocr = recognition.WaybillInfo(
        first_screen_path,
        end_screen_path)
    waybill_screens_id = uuid.uuid4()
    media_url = 'hercules_app\\media\\%s' % waybill_screens_id
    loading_city = get_loading_city(ocr)
    loading_spedition = get_loading_spedition(ocr)
    unloading_city = get_unloading_city(ocr)
    unloading_spedition = get_unloading_spedition(ocr)
    cargo = get_cargo(ocr)
    tonnage = get_tonnage(ocr)
    distance = get_distance(ocr)
    fuel = get_fuel(ocr)
    income = get_income(ocr)
    save_cargo_screen(ocr, waybill_screens_id)
    save_distance_screen(ocr, waybill_screens_id)
    save_fuel_screen(ocr, waybill_screens_id)
    save_income_screen(ocr, waybill_screens_id)
    save_loading_info_screen(ocr, waybill_screens_id)
    save_tonnage_screen(ocr, waybill_screens_id)
    save_unloading_info_screen(ocr, waybill_screens_id)

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
        'loading_info_image': media_url + 'loading-info.png',
        'unloading_info_image': media_url + 'unloading-info.png',
        'cargo_image': media_url + 'cargo.png',
        'tonnage_image': media_url + 'tonnage.png',
        'distance_image': media_url + 'distance.png',
        'fuel_image': media_url + 'fuel.png',
        'income_image': media_url + 'income.png',
    }
    return waybill
