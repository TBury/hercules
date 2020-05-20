from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from hercules_app.models import Driver, DriverStatistics, Achievement
from .forms import CreateUserForm


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            driver = Driver(user=user)
            driver.save()
            statistics = DriverStatistics(driver_id=driver.id)
            statistics.save()
            achievements = Achievement(driver=driver)
            achievements.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('hello')
        else:
            form = CreateUserForm()
    context = {'form': form}
    return render(request, 'register/register.html', context=context)


def logout_user(response):
    logout(response)
    return redirect('index')
