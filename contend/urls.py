from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from contend import views
urlpatterns = [
    
    path('', views.index ,name="index"),
    path('add_conductor/', views.add_conductor ,name="add_conductor"),
    path('add_bus/', views.add_bus ,name="add_bus"),
    path('add_ruta/', views.add_ruta ,name="add_ruta"),
    path('add_calle/', views.add_calle ,name="add_calle"),

	path('list_conductores/', views.list_conductores ,name="list_conductores"),
    path('list_buses/', views.list_buses ,name="list_buses"),
    path('list_rutas/', views.list_rutas ,name="list_rutas"),
    path('list_calles/', views.list_calles ,name="list_calles"),
]