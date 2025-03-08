from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_file, name='home'),  # Главная страница
    path('', views.load_file, name='load_file'),  # Главная страница для загрузки файла и подсчета
    path('clear-memory/', views.clear_memory, name='clear_memory'),
]
