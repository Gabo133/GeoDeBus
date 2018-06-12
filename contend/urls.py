from django.urls import path
from contend import views

urlpatterns = [
    path('', views.index, name="index"),
    path('bus', views.bus, name="bus"),
    path('agregarBus', views.agregarBus, name="agregarBus"),
    path('conductor', views.conductor, name="conductor"),
    path('agregarConductor', views.agregarConductor, name="agregarConductor"),
    path('ruta', views.ruta, name="ruta"),
    path('agregarRuta', views.agregarRuta, name="agregarRuta"),
]
