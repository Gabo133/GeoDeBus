from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from contend.models import Bus, Conductor,Ruta
from django.shortcuts import redirect
from contend.forms import BusForm, SerialGpsForm, EditarBusForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login/login')
def index(request):
	template_name = "index.html"
	data = {}
	return render(request, template_name, data)

@login_required(login_url='/login/login')
def bus(request):
	if request.method == 'POST':
		if request.POST['action'] == 'datatable':
			data = []
			if request.POST['search[value]'] == '':
				query = Bus.objects.filter(habilitado=True)[int(request.POST['start']):int(
					request.POST['start']) + int(request.POST['length'])]
				json = {"recordsTotal": Bus.objects.filter(habilitado=True).count(),
                                    "recordsFiltered": Bus.objects.filter(habilitado=True).count()}
			else:
				query = Bus.objects.filter(Q(patente__icontains=request.POST['search[value]']) | 
										   Q(modelo__icontains=request.POST['search[value]']) | 
										   Q(color__icontains=request.POST['search[value]'])) 
				json = {"recordsTotal": query.count(),
						"recordsFiltered": query.count()}
			for x in query:
				conductor = 'Sin asignar'
				estado = '<span class="role admin">En Terminal</span>'
				if x.getRelacionConBus():
					conductor = x.getRelacionConBus().conductor
					conductor = conductor.nombre + ' ' + conductor.apellido
				if x.estado:
					estado = '<span class="role member">En terreno</span>'
				data.append({'Patente': x.patente,
                             'Conductor': conductor,
							 'Modelo': x.modelo,
							 'Color': x.color,
                             'Estado': estado,
                             'Accion': '<div data-pk=' + str(x.pk) +'>\
							 				<button class="btn-sm btn-success ver">Ver</button> \
											<button class="btn-sm btn-primary editar">Editar</button> \
											<button class="btn-sm btn-danger deshabilitar">Deshabilitar</button> \
										</div>'
							 			})
			json['data'] = data
			return JsonResponse(json)
		elif request.POST['action'] == 'deshabilitar':
		    Bus.objects.get(pk=request.POST['pk']).setHabilitado(False)
		    return JsonResponse({})
		elif request.POST['action'] == 'ver_editar':
			busObj = Bus.objects.get(pk=request.POST['pk'])
			conductor = 'Sin asignar'
			if busObj.getRelacionConBus():
					conductor = busObj.getRelacionConBus().conductor.nombre
			return JsonResponse({'conductor': conductor,
								 'modelo': busObj.modelo,
								 'color': busObj.color,
                            	 'fechaVencimiento': busObj.fechaVencimiento,
                            	 'habilitado': busObj.habilitado,
                            	 'serial': busObj.serialGps.serial})
		elif request.POST['action'] == 'editar':
			busObj = Bus.objects.get(pk=request.POST['pk'])
			formBus = EditarBusForm(request.POST, instance=busObj)
			if formBus.is_valid():
				formBus.save()
				return JsonResponse({"Respuesta": True})
			return JsonResponse({"Respuesta": False})
	template_name = "bus.html"
	formBus = BusForm()
	return render(request, template_name, {'formBus': formBus})

@login_required(login_url='/login/login')
def agregarBus(request):
	formBus = BusForm()
	if request.POST:
		formSerialGps = SerialGpsForm(request.POST)
		if formSerialGps.is_valid():
			formBus = BusForm(request.POST)
			if formBus.is_valid():
				formSerialGps = formSerialGps.save()
				formBus = formBus.save(commit=False)
				formBus.empresa = request.user.empresa
				formBus.serialGps = formSerialGps
				formBus.save()
				return redirect('bus')
	template_name = 'agregarBus.html'
	return render(request, template_name, {'formBus': formBus})

@login_required(login_url='/login/login')
def conductor(request):
	if request.method == 'POST':
		if request.POST['action'] == 'datatable':
			data = []
			if request.POST['search[value]'] == '':
				query = Conductor.objects.filter(empresa=request.user.empresa)[int(request.POST['start']):int(
					request.POST['start']) + int(request.POST['length'])]
				json = {"recordsTotal": Conductor.objects.filter(empresa=request.user.empresa).count(),
                                    "recordsFiltered": Conductor.objects.filter(empresa=request.user.empresa).count()}
			else:
				query = Conductor.objects.filter(Q(nombre__icontains=request.POST['search[value]']) |
                                     Q(apellido__icontains=request.POST['search[value]']) |
                                     Q(rut__icontains=request.POST['search[value]']) |
                                     Q(dv__icontains=request.POST['search[value]']))
				json = {"recordsTotal": query.count(),
						"recordsFiltered": query.count()}
			for x in query:
				bus = 'Sin asignar'
				estado = '<span class="role admin">En Terminal</span>'
				if x.getRelacionConBus():
					lista_buses = x.getRelacionConBus()
					bus = ''
					for i in lista_buses:
						bus += i.bus.patente + ' -'
						if i.bus.estado:
							estado = '<span class="role member">En terreno</span>'
				data.append({'Rut': x.rut,
							 'Nombre': x.nombre + ' ' + x.apellido,
							 'Telefono': x.telefono,
                                    'Bus': bus[0:-2],
							 'Estado': estado,
							 'Accion': '<div data-pk=' + str(x.pk) + '>\
									        <button class="btn-sm btn-primary editar">Editar</button> \
									        <button class="btn-sm btn-danger deshabilitar">Deshabilitar</button> \
								        </div>'
                 })
			json['data'] = data
			return JsonResponse(json)
	template_name = 'conductor.html'
	return render(request, template_name, {})

@login_required(login_url='/login/login')
def ruta(request):
	template_name = 'ruta.html'
	bus = Bus.objects.all()
	print(bus)
	return render(request, template_name, {})	