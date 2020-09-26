from rest_framework import routers
from .api import BondViewset
from django.urls import path, re_path
from bonds import api

urlpatterns = [
    path('bonds/', api.BondViewset.as_view()),
]
