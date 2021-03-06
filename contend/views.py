from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from contend.models import Bus, Conductor, ConductorBus, Ruta, Calle
from django.shortcuts import redirect
from contend.forms import BusForm, SerialGpsForm, EditarBusForm, ConductorForm, RutaForm
from django.db.models import Q
from json import dumps
from django.db import connections
import MySQLdb
from time import sleep
from contend.getest import vehiculo1, vehiculo2
from django.contrib.auth.decorators import login_required


def ejemploBus(request, A, B):
    print(A, B)
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="1234",
                         db="GEODB")
    cur = db.cursor()
    for x, i in zip(vehiculo1, vehiculo2):
        cur.execute("UPDATE contend_gps SET lat=%s, lng=%s WHERE serial='%s' " % (
            x[0], x[1], A))
        cur.execute("UPDATE contend_gps SET lat=%s, lng=%s WHERE serial='%s' " % (
            i[0], i[-1], B))
        db.commit()
        sleep(3)
    db.close()
    return JsonResponse({})


@login_required(redirect_field_name='auth_login')
def index(request):
    data = {}
    data['gpsBus'] = Bus.objects.filter(
        empresa=request.user.empresa, habilitado=True)
    if request.POST:
        if request.POST['action'] == 'update':
            localizacion = []
            cont = 1
            for x in data['gpsBus']:
                localizacion.append(
                    [x.patente, x.serialGps.lat, x.serialGps.lng, cont, x.getNombreConductor()])
                cont += 1
            return JsonResponse({'localizacion': localizacion})
    template_name = "index.html"
    data['totalBus'] = Bus.objects.filter(empresa=request.user.empresa).count()
    data['totalConductor'] = Conductor.objects.filter(
        empresa=request.user.empresa).count()
    data['enRuta'] = Bus.objects.filter(
        empresa=request.user.empresa, estado=True).count()
    data['totalRuta'] = Ruta.objects.filter(
        empresa=request.user.empresa).count()
    return render(request, template_name, data)


@login_required(redirect_field_name='auth_login')
def bus(request):
    if request.method == 'POST':
        if request.POST['action'] == 'datatable':
            data = []
            if request.POST['search[value]'] == '':
                query = Bus.objects.filter(empresa=request.user.empresa)[int(request.POST['start']):int(
                    request.POST['start']) + int(request.POST['length'])]
                json = {"recordsTotal": Bus.objects.all().count(),
                        "recordsFiltered": Bus.objects.all().count()}
            else:
                query = Bus.objects.filter(Q(patente__icontains=request.POST['search[value]']),
                                           empresa=request.user.empresa)
                json = {"recordsTotal": query.count(),
                        "recordsFiltered": query.count()}
            for x in query:
                conductor = 'Sin asignar'
                estado = '<span class="red">En Terminal</span>'
                habilitado = '<button class="btn-sm btn-warning habilitar">Habilitar</button>'
                if x.getRelacionConBus():
                    conductor = x.getRelacionConBus().conductor
                    conductor = conductor.nombre + ' ' + conductor.apellido
                if x.estado:
                    estado = '<span class="green">En terreno</span>'
                if x.habilitado:
                    habilitado = '<button class="btn-sm btn-danger deshabilitar">Deshabilitar</button>'
                data.append({'Patente': x.patente,
                             'Conductor': conductor,
                             'Modelo': x.modelo,
                             'Color': x.color,
                             'Estado': estado,
                             'Accion': '<div data-pk=' + str(x.pk) + '>\
                                            <button class="btn-sm btn-success editar mr-2">Ver</button>\
                                            <button class="btn-sm btn-warning mr-2 asignar">Asignar Ruta</button>'
                             + habilitado +
                             '</div>'
                             })
            json['data'] = data
            return JsonResponse(json)
        elif request.POST['action'] == 'deshabilitar':
            busObj = Bus.objects.get(empresa=request.user.empresa,
                                     pk=request.POST['pk'])
            busObj.habilitado = False
            busObj.estado = False
            busObj.save()
            return JsonResponse({})
        elif request.POST['action'] == 'habilitar':
            Bus.objects.get(empresa=request.user.empresa,
                            pk=request.POST['pk']).setHabilitado(True)
            return JsonResponse({})
        elif request.POST['action'] == 'ver_editar':
            busObj = Bus.objects.get(empresa=request.user.empresa,
                                     pk=request.POST['pk'])
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
            busObj = Bus.objects.get(empresa=request.user.empresa,
                                     pk=request.POST['pk'])
            formBus = EditarBusForm(request.POST, instance=busObj)
            if formBus.is_valid():
                formBus.save()
                return JsonResponse({"Respuesta": True})
            return JsonResponse({"Respuesta": False})

        elif request.POST['action'] == 'verRuta':
            json = {'seleccionado': []}
            rutaObjs = Ruta.objects.filter(empresa=request.user.empresa)
            rutaDisponibleLista = []
            busObj = Bus.objects.get(empresa=request.user.empresa,
                                     pk=request.POST['pk'])
            rutaOriginal = busObj.getRuta()
            if rutaOriginal:
                rutaDisponibleLista.append(
                    {'id': rutaOriginal.pk, 'text': rutaOriginal.nombre})
                json['seleccionado'] = [rutaOriginal.pk, rutaOriginal.nombre]
            for x in rutaObjs:
                rutaDisponibleLista.append({'id': x.pk, 'text': x.nombre})
            json['rutas'] = rutaDisponibleLista
            return JsonResponse(json)
        elif request.POST['action'] == 'asignarRuta':
            busaObj = Bus.objects.get(pk=request.POST['pk'])
            busaObj.setRuta(request.POST['pkRuta'])
            return JsonResponse({})
    template_name = "bus.html"
    formBus = BusForm()
    return render(request, template_name, {'formBus': formBus})


@login_required(redirect_field_name='auth_login')
def agregarBus(request):
    data = {}
    data['formBus'] = BusForm()
    if request.POST:
        data['formSerialGps'] = SerialGpsForm(request.POST)
        data['formBus'] = BusForm(request.POST)
        if data['formSerialGps'].is_valid():
            if data['formBus'].is_valid():
                data['formSerialGps'] = data['formSerialGps'].save()
                data['formBus'] = data['formBus'].save(commit=False)
                data['formBus'].empresa = request.user.empresa
                data['formBus'].serialGps = data['formSerialGps']
                data['formBus'].save()
                return redirect('bus')
    template_name = 'agregarBus.html'
    return render(request, template_name, data)


@login_required(redirect_field_name='auth_login')
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
                                                 Q(dv__icontains=request.POST['search[value]'],
                                                   empresa=request.user.empresa))
                json = {"recordsTotal": query.count(),
                        "recordsFiltered": query.count()}
            for x in query:
                bus = 'Sin asignar'
                estado = '<span class="red">En Terminal</span>'
                habilitado = '<button class="btn-sm btn-warning habilitar">Habilitar</button>'
                if x.getRelacionConBus():
                    bus = x.getRelacionConBus().bus
                    if bus.estado:
                        estado = '<span class="green">En terreno</span>'
                    bus = bus.patente
                if x.habilitado:
                    habilitado = '<button class="btn-sm btn-danger deshabilitar">Deshabilitar</button>'
                data.append({'Rut': str(x.rut) + '-' + str(x.dv),
                             'Nombre': x.nombre + ' ' + x.apellido,
                             'Telefono': x.telefono,
                             'Bus': bus,
                             'Estado': estado,
                             'Accion': '<div data-pk=' + str(x.pk) + '>\
                                            <button class="btn-sm btn-success mr-1 editar">Ver</button> \
                                            <button class="btn-sm btn-warning mr-2 asignar">Asignar Bus</button>'
                             + habilitado +
                             '</div>'
                             })
            json['data'] = data
            return JsonResponse(json)
        elif request.POST['action'] == 'deshabilitar':
            conductorObj = Conductor.objects.get(empresa=request.user.empresa,
                                                 pk=request.POST['pk'])
            conductorObj.habilitado = False
            conductorObj.estado = False
            conductorObj.save()
            return JsonResponse({})
        elif request.POST['action'] == 'habilitar':
            conductorObj = Conductor.objects.get(empresa=request.user.empresa,
                                                 pk=request.POST['pk']).setHabilitado(True)
            return JsonResponse({})
        elif request.POST['action'] == 'editar':
            conductorObj = Conductor.objects.get(empresa=request.user.empresa,
                                                 pk=request.POST['pk'])
            formConductor = ConductorForm(request.POST, instance=conductorObj)
            if formConductor.is_valid():
                formConductor.save()
                return JsonResponse({"Respuesta": True})
            return JsonResponse({"Respuesta": False})
        elif request.POST['action'] == 'ver_editar':
            conductorObj = Conductor.objects.get(empresa=request.user.empresa,
                                                 pk=request.POST['pk'])
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
            conductorObj = Conductor.objects.get(empresa=request.user.empresa,
                                                 pk=request.POST['pk'])
            if conductorObj:
                if conductorObj.getRelacionConBus():
                    bus = conductorObj.getRelacionConBus().bus
                    busDisponibleLista.append(
                        {'id': bus.pk, 'text': bus.patente})
                    json['seleccionado'] = [bus.pk, bus.patente]
            for x in busDisponible:
                busDisponibleLista.append({'id': x.pk, 'text': x.patente})
            json['buses'] = busDisponibleLista
            return JsonResponse(json)
        elif request.POST['action'] == 'asignarBus':
            conductorObj = Conductor.objects.get(empresa=request.user.empresa,
                                                 pk=request.POST['pk'])
            conductorObj.asignarBus(request.POST['pkBus'])
            return JsonResponse({})
    formConductor = ConductorForm()
    template_name = 'conductor.html'
    return render(request, template_name, {'formConductor': formConductor})


@login_required(redirect_field_name='auth_login')
def agregarConductor(request):
    data = {}
    data['formConductor'] = ConductorForm()
    if request.POST:
        data['formConductor'] = ConductorForm(request.POST)
        if data['formConductor'].is_valid():
            data['formConductor'] = data['formConductor'].save(commit=False)
            data['formConductor'].empresa = request.user.empresa
            data['formConductor'].save()
            return redirect('conductor')
    template_name = 'agregarConductor.html'
    return render(request, template_name, data)


@login_required(redirect_field_name='auth_login')
def ruta(request):
    if request.method == 'POST':
        if request.POST['action'] == 'datatable':
            data = []
            if request.POST['search[value]'] == '':
                query = Ruta.objects.all()[int(request.POST['start']):int(
                    request.POST['start']) + int(request.POST['length'])]
                json = {"recordsTotal": Ruta.objects.all().count(),
                        "recordsFiltered": Ruta.objects.all().count()}
            else:
                query = Ruta.objects.filter(Q(nombre__icontains=request.POST['search[value]']),
                                            empresa=request.user.empresa)
                json = {"recordsTotal": query.count(),
                        "recordsFiltered": query.count()}
            for x in query:
                habilitado = '<button class="btn-sm btn-warning habilitar">Habilitar</button>'
                if x.habilitado:
                    habilitado = '<button class="btn-sm btn-danger deshabilitar">Deshabilitar</button>'
                data.append({'Nombre': x.nombre,
                             'Buses': 'Total: ' + str(x.busruta_set.all().count()) + ' Bus(es)',
                             'Accion': '<div data-pk=' + str(x.pk) + '>\
                                            <button class="btn-sm btn-success ver mr-1">Ver Ruta</button> \
                                            <a href="' + reverse('editarRuta', kwargs={'idRuta': x.pk}) + '" class="btn-sm btn-primary mr-2">Editar</a >'
                             + habilitado +
                             '</div>'
                             })
            json['data'] = data
            return JsonResponse(json)
        elif request.POST['action'] == 'deshabilitar':
            Ruta.objects.get(pk=request.POST['pk'],
                             empresa=request.user.empresa).setHabilitado(False)
            return JsonResponse({})
        elif request.POST['action'] == 'habilitar':
            Ruta.objects.get(pk=request.POST['pk'],
                             empresa=request.user.empresa).setHabilitado(True)
            return JsonResponse({})
        elif request.POST['action'] == 'cargarRuta':
            calles = Ruta.objects.get(pk=request.POST['pk'],
                                      empresa=request.user.empresa).calle_set.all()
            posiciones = []
            for x in calles:
                posiciones.append({'lat': x.lat, 'lng': x.lng})
            return JsonResponse({'posiciones': posiciones})
    template_name = 'ruta.html'
    return render(request, template_name, {})


@login_required(redirect_field_name='auth_login')
def agregarRuta(request):
    if request.POST:
        calleInicial = request.POST.getlist('calle[]')[0]
        calleFinal = request.POST.getlist('calle[]')[-1]
        calleInicial = calleInicial.split(',')
        calleFinal = calleFinal.split(',')
        calleInicial = [float(calleInicial[0]), float(calleInicial[1])]
        calleFinal = [float(calleFinal[0]), float(calleFinal[1])]
        rutaObj = Ruta.objects.create(empresa=request.user.empresa,
                                      nombre=request.POST['nombre'],
                                      latInicial=calleInicial[0],
                                      lngInicial=calleInicial[1],
                                      latFinal=calleFinal[0],
                                      lngFinal=calleFinal[1])
        for x in request.POST.getlist('calle[]'):
            coordenadas = x.split(',')
            rutaObj.addCalle(coordenadas[0], coordenadas[1])
        return JsonResponse({})
    template_name = 'agregarRuta.html'
    formRuta = RutaForm()
    return render(request, template_name, {'formRuta': formRuta})


@login_required(redirect_field_name='auth_login')
def editarRuta(request, idRuta):
    rutaObj = Ruta.objects.get(pk=idRuta)
    if request.POST:
        calleInicial = request.POST.getlist('calle[]')[0]
        calleFinal = request.POST.getlist('calle[]')[-1]
        calleInicial = calleInicial.split(',')
        calleFinal = calleFinal.split(',')
        calleInicial = [float(calleInicial[0]), float(calleInicial[1])]
        calleFinal = [float(calleFinal[0]), float(calleFinal[1])]
        rutaObj.reasignarCalle()
        rutaObj.nombre = request.POST['nombre']
        rutaObj.latInicial = calleInicial[0]
        rutaObj.lngInicial = calleInicial[1]
        rutaObj.latFinal = calleFinal[0]
        rutaObj.lngFinal = calleFinal[1]
        for x in request.POST.getlist('calle[]'):
            coordenadas = x.split(',')
            rutaObj.addCalle(coordenadas[0], coordenadas[1])
        return JsonResponse({})
    template_name = 'editarRuta.html'
    formRuta = RutaForm(instance=rutaObj)
    return render(request, template_name, {'formRuta': formRuta,
                                           'ruta': rutaObj,
                                           'ini': rutaObj.latInicial,
                                           'fin': rutaObj.lngInicial})
