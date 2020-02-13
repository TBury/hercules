from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from hercules_app.models import Driver
from hercules_app.forms import SetNickForm

def index(request):
    return render(request, 'hercules_app/index.html')

def login(request):
    return render(request, 'hercules_app/sign-in.html')

@login_required
#TODO: create test for checking if the user
# nick or not
def hello (request):
    current_user = request.user
    form = SetNickForm()
    if request.method == "POST":
        form = SetNickForm(request.POST)
        if form.is_valid():
            Driver.objects.filter(user=current_user).update(nick=form.data['nick'])
            return redirect('success')
        else:
            form = SetNickForm()
    return render(request, 'hercules_app/hello.html')


@login_required
def success(request):
    return render(request, 'hercules_app/success.html')
