from django.contrib import admin
from .models import Empresa, Bus, Conductor, Ruta, Calle
# Register your models here.
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
	list_display = ('Nombre','Rut')

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
	list_display = ('Patente', 'Modelo')

@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
	list_display = ('Nombre', 'Rut')

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
	pass

@admin.register(Calle)
class CalleAdmin(admin.ModelAdmin):
	pass
