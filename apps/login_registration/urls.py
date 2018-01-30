#Login URLs
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/validation', views.LoginValidator),
    url(r'registration/validation', views.RegistrationValidator),
    url(r'^', views.index),
]