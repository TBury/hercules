from django.urls import path
from . import views
from register import views as register_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(
        template_name="hercules_app/sign-in.html",
        extra_context={
            'next': '/panel',
        }, redirect_authenticated_user=True), name='login'),
    path('register', register_views.register, name='register'),
    path('hello', views.hello, name='hello'),
    path('logout', register_views.logout_user, name='logout'),
    path('success', views.success, name="success"),
]
