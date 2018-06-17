from django.db import models
from django.contrib.auth.models import User
from contend.choices import choice_dv
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    rut = models.PositiveIntegerField()
    dv = models.CharField(max_length=1,
                          choices=choice_dv)


class Conductor(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    rut = models.PositiveIntegerField()
    dv = models.CharField(max_length=1,
                          choices=choice_dv)
    fechaNacimiento = models.DateField()
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    fechaVencimiento = models.DateField()
    habilitado = models.BooleanField(default=True)

    def getRelacionConBus(self):
        try:
            return self.conductorbus
        except ObjectDoesNotExist:
            return None

    def setHabilitado(self, habilitado):
        self.habilitado = habilitado
        self.save()

    def eliminarBus(self):
        self.conductorbus.delete()
        return

    def asignarBus(self, patente):
        if self.getRelacionConBus():
            self.eliminarBus()
        return ConductorBus.objects.create(bus=Bus.objects.get(patente=patente),
                                           conductor=self)

    def getNombreCompleto(self):
        return '%s %s' % (self.nombre, self.apellido)


class ConductorBus(models.Model):
    bus = models.OneToOneField("Bus", on_delete=models.CASCADE)
    conductor = models.OneToOneField("Conductor", on_delete=models.CASCADE)


class Bus(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    serialGps = models.OneToOneField("Gps", on_delete=models.CASCADE)
    patente = models.CharField(max_length=7, primary_key=True)
    modelo = models.CharField(max_length=20)
    color = models.CharField(max_length=15)
    fechaVencimiento = models.DateField()
    estado = models.BooleanField(default=False)
    habilitado = models.BooleanField(default=True)

    def getRelacionConBus(self):
        try:
            return self.conductorbus
        except ObjectDoesNotExist:
            return None

    def setHabilitado(self, habilitado):
        self.habilitado = habilitado
        self.save()

    def getRuta(self):
        try:
            return self.busruta.ruta
        except ObjectDoesNotExist:
            return None

    def setRuta(self, ruta):
        rutaObj = Ruta.objects.get(pk=ruta)
        return BusRuta.objects.create(bus=self, ruta=rutaObj)

    def getNombreConductor(self):
        try:
            return self.conductorbus.conductor.getNombreCompleto()
        except ObjectDoesNotExist:
            return 'Sin Asignar'


class Gps(models.Model):
    serial = models.CharField(max_length=20, primary_key=True)
    lat = models.FloatField(default=-33.448890)
    lng = models.FloatField(default=-70.669265)


class Historial(models.Model):
    gps = models.ForeignKey("Gps", on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True)
    lat = models.FloatField()
    lng = models.FloatField()


class BusRuta(models.Model):
    bus = models.OneToOneField("Bus", on_delete=models.CASCADE)
    ruta = models.ForeignKey("Ruta", on_delete=models.CASCADE)


class Ruta(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    latInicial = models.FloatField()
    lngInicial = models.FloatField()
    latFinal = models.FloatField()
    lngFinal = models.FloatField()
    habilitado = models.BooleanField(default=True)

    def setHabilitado(self, habilitado):
        self.habilitado = habilitado
        self.save()

    def addCalle(self, lat, lng):
        return Calle.objects.create(ruta=self, lat=float(lat), lng=float(lng))

    def __str__(self):
        return "Nombre: %s, LatIni: %s, LngIni: %s, LatFinal: %s, LngFinal: %s" % (self.nombre, self.latInicial, self.lngInicial, self.latFinal, self.lngFinal)

    def reasignarCalle(self):
        self.calle_set.all().delete()
        return


class Calle(models.Model):
    ruta = models.ForeignKey("Ruta", on_delete=models.CASCADE)
    lat = models.FloatField()
    lng = models.FloatField()
