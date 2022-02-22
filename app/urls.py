from django.contrib import admin
from django.urls import path
from .views import *

app_name = "app"

urlpatterns = [
    path('signup',Signup),
]
