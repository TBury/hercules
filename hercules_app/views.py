from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.decorators import user_passes_test
from hercules_app.models import Driver, Company, DriverStatistics, Vehicle, Disposition, Waybill
from hercules_app.forms import SetNickForm, FirstScreenshotForm, SecondScreenshotForm, AddWaybillForm
from django.utils.encoding import smart_str
from .tasks import get_waybill_info
from django_celery_results.models import TaskResult


def index(request):
    return render(request, 'hercules_app/index.html')


def login(request):
    return render(request, 'hercules_app/sign-in.html')


@login_required
# TODO: create test for checking if the user
# nick or not
def hello(request):
    current_user = request.user
    form = SetNickForm()
    if request.method == "POST":
        form = SetNickForm(request.POST)
        if form.is_valid():
            Driver.objects.filter(user=current_user).update(
                nick=form.data['nick'])
            return redirect('panel')
        form = SetNickForm()
    return render(request, 'hercules_app/hello.html')


@login_required
def panel(request):
    driver = Driver.objects.get(user=request.user)
    statistics = DriverStatistics.objects.get(driver_id=driver)
    if driver.company_id is not None:
        company = Company.objects.get(id=driver.company_id)
    company = ""
    try:
        vehicle = Vehicle.objects.get(driver=driver)
    except:
        vehicle = ""

    dispositions = Disposition.objects.filter(driver=driver)[:3]
    args = {
        'driver': driver,
        'company': company,
        'statistics': statistics,
        'vehicle': vehicle,
        'dispositions': dispositions
    }
    return render(request, 'hercules_app/panel.html', args)


@login_required
def download_assistant(request):
    args = Driver.get_username(request.user)
    return render(request, 'hercules_app/download.html', args)


def download_file(request):
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(
        'assistant.zip')

    response['X-Sendfile'] = smart_str('assistant.zip')
    return response


def drivers_card(request):
    driver = Driver.objects.get(user=request.user)
    statistics = DriverStatistics.objects.get(driver_id=driver)
    if driver.company_id is not None:
        company = Company.objects.get(id=driver.company_id)
    company = ""
    if driver.vehicle_id is not None:
        vehicle = Vehicle.objects.get(driver=driver)
    vehicle = ""
    dispositions = Disposition.objects.filter(driver=driver)[:5]
    args = {
        'driver': driver,
        'company': company,
        'statistics': statistics,
        'dispositions': dispositions
    }
    if vehicle is not None:
        args += {'vehicle': vehicle}
    return render(request, 'hercules_app/drivers-card.html', args)


def add_delivery(request):
    driver = Driver.objects.get(user=request.user)
    args = {
        'driver': driver,
    }
    return render(request, 'hercules_app/add_delivery.html', args)


def send_first_screenshot(request):
    if request.method == 'POST':
        form = FirstScreenshotForm(request.POST, request.FILES)
        if form.is_valid():
            waybill = form.save()
            request.session['waybill_id'] = waybill.id
        else:
            form = FirstScreenshotForm()
    return render(request, 'hercules_app/automatic_1.html')


def send_second_screenshot(request):
    waybill_id = request.session.get('waybill_id')
    # TODO: check if the waybill_id is passed correctly
    waybill = Waybill.objects.get(id=waybill_id)
    if request.method == "POST":
        form = SecondScreenshotForm(
            request.POST, request.FILES, instance=waybill)
        if form.is_valid():
            form.save()
    else:
        form = SecondScreenshotForm()
    return render(request, 'hercules_app/automatic_2.html')


def add_waybill(request):
    waybill_id = request.session.get('waybill_id')
    # TODO: check if the waybill_id is passed correctly
    waybill = Waybill.objects.get(id=waybill_id)
    info = get_waybill_info.delay(waybill.first_screen.path,
                                  waybill.end_screen.path)
    args = info.get()
    if request.method == "POST":
        form = AddWaybillForm(
            request.POST, request.FILES, instance=waybill)
        if form.is_valid():
            form.save()
    else:
        form = AddWaybillForm()
    return render(request, 'hercules_app/verify.html', args)
