from django.urls import path, re_path

from .views import *
urlpatterns = [
    re_path('^book/$', BookView.as_view()),
    path('bookdetail/', BookDetailView.as_view()),

    path('v2/book/', V2BookView.as_view()), # 序列化与反序列化整合
    path('v2/book/<int:pk>/', V2BookView.as_view())
]