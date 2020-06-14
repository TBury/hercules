import uuid
from io import BytesIO
from celery import task
from celery.utils.log import get_task_logger
from hercules_app import recognition
from hercules_app.models import TruckersMPStatus, CompanySettings, WaybillImages, Waybill, Gielda, Disposition
from django.core.files.base import ContentFile
from random import randint
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
    screen_id = uuid.uuid4()
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

    loading_info = create_temp_image(ocr.get_loading_info_image())
    unloading_info = create_temp_image(ocr.get_unloading_info_image())
    cargo_image = create_temp_image(ocr.get_cargo_image())
    tonnage_image = create_temp_image(ocr.get_tonnage_image())
    distance_image = create_temp_image(ocr.get_distance_image())
    fuel_image = create_temp_image(ocr.get_fuel_image())
    income_image = create_temp_image(ocr.get_income_image())


    loading_info_name = f"{screen_id}-linfo.png"
    unloading_info_name = f"{screen_id}-uinfo.png"
    cargo_image_name = f"{screen_id}-cinfo.png"
    tonnage_image_name = f"{screen_id}-tinfo.png"
    distance_image_name = f"{screen_id}-dinfo.png"
    fuel_image_name = f"{screen_id}-finfo.png"
    income_image_name = f"{screen_id}-iinfo.png"


    WaybillImages.objects.create(
        waybill=w,
        loading_info=ContentFile(loading_info, loading_info_name),
        unloading_info=ContentFile(unloading_info, unloading_info_name),
        cargo_image=ContentFile(cargo_image, cargo_image_name),
        tonnage_image=ContentFile(tonnage_image, tonnage_image_name),
        distance_image=ContentFile(distance_image, distance_image_name),
        fuel_image=ContentFile(fuel_image, fuel_image_name),
        income_image=ContentFile(income_image, income_image_name),
    )

    return waybill


def create_temp_image(image):
    temp_image = BytesIO()
    image.save(temp_image, "PNG")
    return temp_image.getvalue()


@task (
    name="get-status",
    ignore_result=True
)
def get_tmp_server_status():
    TruckersMPStatus.save_status_to_database()

@task (
    name="create-new-offers",
    ignore_result=True
)
def create_offers():
    for i in range(50):
        offer = Disposition.create_disposition()
        Gielda.objects.create(
            loading_city=offer.get("loading_city"),
            unloading_city=offer.get("unloading_city"),
            loading_country=offer.get("loading_country"),
            unloading_country=offer.get("unloading_country"),
            loading_spedition=offer.get("loading_spedition"),
            unloading_spedition=offer.get("unloading_spedition"),
            cargo=offer.get("cargo"),
            tonnage=offer.get("tonnage"),
            adr=offer.get("adr"),
            price=randint(5000, 100000)
        )


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