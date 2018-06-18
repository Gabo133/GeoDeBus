from django.urls import path
from contend import views
urlpatterns = [
    path('', views.index, name="index"),
    path('bus', views.bus, name="bus"),
    path('agregarBus', views.agregarBus, name="agregarBus"),
    path('conductor', views.conductor, name="conductor"),
    path('ruta', views.ruta, name="ruta"),
    path('agregarConductor', views.agregarConductor, name="agregarConductor"),
    path('agregarRuta', views.agregarRuta, name="agregarRuta"),
    path('editarRuta/<int:idRuta>/', views.editarRuta, name="editarRuta"),
    path('ejemploBus/<int:A>/<int:B>', views.ejemploBus, name="ejemploBus"),
]
