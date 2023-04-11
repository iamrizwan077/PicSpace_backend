from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path("", views.gallery, name="gallery"),
    path("get_token", views.get_token, name="get_token"),
]
