from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_demo, name='menu_demo'),
]
