from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_file, name='load_file'),
    path('wordcount/', views.word_count, name='word_count'),
    path('clear/', views.clear_memory, name='clear_memory'),
]
