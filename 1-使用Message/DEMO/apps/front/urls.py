from django.urls import path

from .views import *
urlpatterns = [
    path('signin', LoginView.as_view(), name='login')
]