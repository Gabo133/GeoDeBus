from django.contrib import admin
from contend.models import Empresa, Conductor, ConductorBus, Bus, Gps, Historial, Ruta, Calle
# Register your models here.


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    pass


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    pass


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(Gps)
class GpsAdmin(admin.ModelAdmin):
    pass


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    pass


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    pass


@admin.register(Calle)
class CalleAdmin(admin.ModelAdmin):
    pass


@admin.register(ConductorBus)
class ConductorBusAdmin(admin.ModelAdmin):
    pass
