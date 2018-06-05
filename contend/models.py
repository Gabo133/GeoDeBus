from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Empresa(models.Model):
	Nombre = models.CharField(max_length=50)
	Direccion = models.CharField(max_length=100)
	Telefono = models.CharField(max_length=50)
	Email = models.CharField(max_length=50)
	Rut = models.CharField(max_length=50)
	Id = models.CharField(max_length=50)
	
	def __str__(self):
		return self.Id
class Conductor(models.Model):
	Nombre = models.CharField(max_length=50)
	Apellido = models.CharField(max_length=50)
	Rut = models.CharField(max_length=20)
	FechaNacimiento = models.DateField()
	Direccion = models.CharField(max_length=100)
	Telefono = models.CharField(max_length=50)
	FechaVencimiento = models.DateField()
	Empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, blank=True)
	def __str__(self):
		return self.Rut
class Bus(models.Model):
	
	Patente = models.CharField(max_length=30)
	Color = models.CharField(max_length=30)
	Modelo = models.CharField(max_length=80)
	SerialGps = models.CharField(max_length=80)
	FechaVencimiento = models.DateField()
	Conductor = models.OneToOneField(Conductor, on_delete=models.CASCADE,blank=True)
	def __str__(self):
		return self.Patente

		
class Calle(models.Model):
	Nombre = models.CharField(max_length=100)
	LatInicial = models.CharField(max_length=100)
	LongIcial = models.CharField(max_length = 100)
	LatFinal = models.CharField(max_length=100)
	LongFinal = models.CharField(max_length=100)
	def __str__(self):
		return self.Nombre

class Ruta(models.Model):
	Id = models.CharField(max_length=30)
	Calle = models.ManyToManyField(Calle, blank=True)
	def __str__(self):
		return self.Id


		
		
		
		