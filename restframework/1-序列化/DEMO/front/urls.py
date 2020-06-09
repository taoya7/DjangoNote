from django.urls import path

from .views import *
urlpatterns = [
    path('', PersonView.as_view())
]