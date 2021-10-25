from django.urls import path

from .views      import *

urlpatterns = [
    path('', TheaterView.as_view())
]