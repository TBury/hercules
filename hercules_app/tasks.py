import uuid

from celery import task
from celery.utils.log import get_task_logger

from django.core.files.storage import default_storage as storage
from hercules_app import recognition
from hercules_app.models import TruckersMPStatus, CompanySettings

logger = get_task_logger(__name__)

@task
def get_loading_city(ocr, bind=True):
    loading_city = ocr.get_loading_city()
    return loading_city


@task
def get_loading_spedition(ocr, bind=True):
    loading_spedition = ocr.get_loading_spedition()
    return loading_spedition


@task
def get_unloading_city(ocr, bind=True):
    unloading_city = ocr.get_unloading_city()
    return unloading_city


@task
def get_unloading_spedition(ocr, bind=True):
    unloading_spedition = ocr.get_unloading_spedition()
    return unloading_spedition


@task
def get_cargo(ocr, bind=True):
    cargo = ocr.get_cargo()
    return cargo


@task
def get_tonnage(ocr, bind=True):
    tonnage = ocr.get_tonnage()
    return tonnage


@task
def get_distance(ocr, bind=True):
    distance = ocr.get_distance()
    return distance


@task
def get_fuel(ocr, bind=True):
    fuel = ocr.get_fuel()
    return fuel


@task
def get_income(ocr, bind=True):
    income = ocr.get_income()
    return income


@task
def get_waybill_info(first_screen_path, end_screen_path, bind=True):
    ocr = recognition.WaybillInfo(
        first_screen_path,
        end_screen_path)
    waybill_screens_id = uuid.uuid4()
    media_url = 'waybills/%s' % waybill_screens_id
    loading_city = get_loading_city(ocr)
    loading_spedition = get_loading_spedition(ocr)
    unloading_city = get_unloading_city(ocr)
    unloading_spedition = get_unloading_spedition(ocr)
    cargo = get_cargo(ocr)
    tonnage = get_tonnage(ocr)
    distance = get_distance(ocr)
    fuel = get_fuel(ocr)
    income = get_income(ocr)
    ocr.save_cargo_screen(waybill_screens_id)
    ocr.save_distance_screen(waybill_screens_id)
    ocr.save_fuel_screen(waybill_screens_id)
    ocr.save_income_screen(waybill_screens_id)
    ocr.save_loading_info_screen(waybill_screens_id)
    ocr.save_tonnage_screen(waybill_screens_id)
    ocr.save_unloading_info_screen(waybill_screens_id)


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
        'loading_info_image': media_url + '-loading-info.png',
        'unloading_info_image': media_url + '-unloading-info.png',
        'cargo_image': media_url + '-cargo.png',
        'tonnage_image': media_url + '-tonnage.png',
        'distance_image': media_url + '-distance.png',
        'fuel_image': media_url + '-fuel.png',
        'income_image': media_url + '-income.png',
        'screen_id': waybill_screens_id,
    }
    return waybill


@task (
    name="get-status",
    ignore_result=True
)
def get_tmp_server_status():
    TruckersMPStatus.save_status_to_database()



@task (
    name="random-vehicle-weekly",
    ignore_result=True
)
def random_vehicle_weekly():
    CompanySettings.weekly_random_vehicles()

@task (
    name="random-vehicle-monthly",
    ignore_result=True
)
def random_vehicle_weekly():
    CompanySettings.monthly_random_vehicles()