from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from contend.models import Bus, Conductor, ConductorBus
from django.shortcuts import redirect
from contend.forms import BusForm, SerialGpsForm, EditarBusForm, ConductorForm
from django.db.models import Q

# Create your views here.


def index(request):
    template_name = "index.html"
    data = {}
    return render(request, template_name, data)


def bus(request):
    if request.method == 'POST':
        if request.POST['action'] == 'datatable':
            data = []
            if request.POST['search[value]'] == '':
                query = Bus.objects.filter(eliminado=False)[int(request.POST['start']):int(
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
                habilitado = '<button class="btn-sm btn-warning habilitar">Habilitar</button>'
                if x.getRelacionConBus():
                    conductor = x.getRelacionConBus().conductor
                    conductor = conductor.nombre + ' ' + conductor.apellido
                if x.estado:
                    estado = '<span class="role member">En terreno</span>'
                if x.habilitado:
                    habilitado = '<button class="btn-sm btn-danger deshabilitar">Deshabilitar</button>'
                data.append({'Patente': x.patente,
                             'Conductor': conductor,
                             'Modelo': x.modelo,
                             'Color': x.color,
                             'Estado': estado,
                             'Accion': '<div data-pk=' + str(x.pk) + '>\
                                            <button class="btn-sm btn-success ver mr-1">Ver</button> \
                                            <button class="btn-sm btn-primary editar mr-2">Editar</button>'
                                            + habilitado + \
                                        '</div>'
                             })
            json['data'] = data
            return JsonResponse(json)
        elif request.POST['action'] == 'deshabilitar':
            busObj = Bus.objects.get(pk=request.POST['pk'])
            busObj.habilitado = False
            busObj.estado = False
            busObj.save()
            return JsonResponse({})
        elif request.POST['action'] == 'habilitar':
            busObj = Bus.objects.get(pk=request.POST['pk']).setHabilitado(True)
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
                bus = 'Sin asignar  '
                estado = '<span class="role admin">En Terminal</span>'
                habilitado = '<button class="btn-sm btn-warning habilitar">Habilitar</button>'
                if x.getRelacionConBus():
                    bus = x.getRelacionConBus().bus
                    if bus.estado:
                        estado = '<span class="role member">En terreno</span>'
                    bus = bus.patente
                if x.habilitado:
                    habilitado = '<button class="btn-sm btn-danger deshabilitar">Deshabilitar</button>'
                data.append({'Rut': x.rut,
                             'Nombre': x.nombre + ' ' + x.apellido,
                             'Telefono': x.telefono,
                             'Bus': bus,
                             'Estado': estado,
                             'Accion': '<div data-pk=' + str(x.pk) + '>\
                                            <button class="btn-sm btn-primary mr-1 editar">Editar</button> \
                                            <button class="btn-sm btn-warning mr-2 asignar">Asignar Bus</button>'
                                            + habilitado + 
                                        '</div>'
                             })
            json['data'] = data
            return JsonResponse(json)
        elif request.POST['action'] == 'deshabilitar':
            conductorObj = Conductor.objects.get(pk=request.POST['pk'])
            conductorObj.habilitado = False
            conductorObj.estado = False
            conductorObj.save()
            return JsonResponse({})
        elif request.POST['action'] == 'habilitar':
            conductorObj = Conductor.objects.get(pk=request.POST['pk']).setHabilitado(True)
            return JsonResponse({})
        elif request.POST['action'] == 'editar':
            conductorObj = Conductor.objects.get(pk=request.POST['pk'])
            formConductor = ConductorForm(request.POST, instance=conductorObj)
            if formConductor.is_valid():
                formConductor.save()
                return JsonResponse({"Respuesta": True})
            return JsonResponse({"Respuesta": False})
        elif request.POST['action'] == 'ver_editar':
            conductorObj = Conductor.objects.get(pk=request.POST['pk'])
            return JsonResponse({'rut': conductorObj.rut,
                                 'nombre': conductorObj.nombre,
                                 'apellido': conductorObj.apellido,
                                 'dv': conductorObj.dv,
                                 'fechaNacimiento': conductorObj.fechaNacimiento,
                                 'direccion': conductorObj.direccion,
                                 'telefono': conductorObj.telefono,
                                 'fechaVencimiento': conductorObj.fechaVencimiento})
        elif request.POST['action'] == 'cargarBus':
            json = {'seleccionado': []}
            conductorBus = ConductorBus.objects.all()
            busDisponible = Bus.objects.exclude(conductorbus__in=conductorBus)
            busDisponibleLista = []
            conductorObj = Conductor.objects.get(pk=request.POST['pk'])
            if conductorObj:
                if conductorObj.getRelacionConBus():
                    bus = conductorObj.getRelacionConBus().bus
                    busDisponibleLista.append({'id': bus.pk, 'text': bus.patente})
                    json['seleccionado'] = [bus.pk, bus.patente]
            for x in busDisponible:
                busDisponibleLista.append({'id': x.pk, 'text': x.patente})
            json['buses'] = busDisponibleLista
            return JsonResponse(json)
        elif request.POST['action'] == 'asignarBus':
            conductorObj = Conductor.objects.get(pk=request.POST['pk'])
            conductorObj.asignarBus(request.POST['pkBus'])
            return JsonResponse({})
    formConductor = ConductorForm()
    template_name = 'conductor.html'
    return render(request, template_name, {'formConductor': formConductor})


def agregarConductor(request):
    formConductor = ConductorForm()
    if request.POST:
        formConductor = ConductorForm(request.POST)
        if formConductor.is_valid():
            formConductor = formConductor.save(commit=False)
            formConductor.empresa = request.user.empresa
            formConductor.save()
            return redirect('conductor')

    template_name = 'agregarConductor.html'
    return render(request, template_name, {'formConductor': formConductor})
