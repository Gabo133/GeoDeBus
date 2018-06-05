from django.shortcuts import render
from contend.models import *
from contend.forms import *
# Create your views here.
def index(request):
	template_name = "index.html"
	data = {}
	return render(request, template_name, data)

#  ---------------------------------- Add -----------------------------------

def add_conductor(request):
	template_name = "index.html"
	data = {}
	return render(request, template_name, data)

def add_bus(request):
	template_name = "index.html"
	data = {}
	return render(request, template_name, data)

def add_ruta(request):
	template_name = "index.html"
	data = {}
	return render(request, template_name, data)

def add_calle(request):
	template_name = "index.html"
	data = {}
	return render(request, template_name, data)

# -------------------------------------- List ----------------------------

def list_conductores(request):
	template_name = "Listar_conductores.html"
	data = {}
	return render(request, template_name, data)

def list_buses(request):
	template_name = "listar_buses.html"
	data = {}
	return render(request, template_name, data)

def list_rutas(request):
	template_name = "listar_rutas.html"
	data = {}
	return render(request, template_name, data)

def list_calles(request):
	template_name = "index.html"
	data = {}
	return render(request, template_name, data)

