from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from contend import views
urlpatterns = [
    
    path('', views.index, name="index"),
    path('bus', views.bus, name="bus"),
    path('agregarBus', views.agregarBus, name="agregarBus"),
    path('conductor', views.conductor, name="conductor"),
    path('ruta', views.ruta, name="ruta"),
]
