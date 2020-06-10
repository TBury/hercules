import uuid
from io import BytesIO
from tempfile import NamedTemporaryFile

from celery import task
from celery.utils.log import get_task_logger
from django.core.files.images import File
from hercules_app import recognition
from hercules_app.models import TruckersMPStatus, CompanySettings, WaybillImages, Waybill
from django.core.files.base import ContentFile
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
def get_waybill_info(first_screen_path, end_screen_path, waybill_id, bind=True):
    w = Waybill.objects.get(id=waybill_id)
    ocr = recognition.WaybillInfo(
        first_screen_path,
        end_screen_path
    )
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

    WaybillImages.objects.create(
        waybill=w,
        loading_info=ContentFile(ocr.get_loading_info_image(), loading_city),
        unloading_info=ContentFile(ocr.get_unloading_info_image(), loading_city),
        cargo_image=ContentFile(ocr.get_cargo_image(), loading_city),
        tonnage_image=ContentFile(ocr.get_tonnage_image(), loading_city),
        distance_image=ContentFile(ocr.get_distance_image(), loading_city),
        fuel_image=ContentFile(ocr.get_fuel_image(), loading_city),
        income_image=ContentFile(ocr.get_income_image(), loading_city),
    )

    return waybill


def create_temp_image(image):
    temp_image = NamedTemporaryFile(delete=True)
    temp_image.write(image.read())
    temp_image.flush()
    return temp_image


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