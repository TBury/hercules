from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from hercules_app.models import Driver, DriverStatistics
from .forms import CreateUserForm


def register(response):
    form = CreateUserForm()
    if response.method == "POST":
        form = CreateUserForm(response.POST)
        if form.is_valid():
            user = form.save()
            driver = Driver(user=user)
            driver.save()
            statistics = DriverStatistics(driver_id=driver.id)
            statistics.save()
            login(response, user)
            return redirect('hello')
        else:
            form = CreateUserForm()
    context = {'form': form}
    return render(response, 'register/register.html', context=context)


def logout_user(response):
    logout(response)
    return redirect('index')
