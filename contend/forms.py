from django import forms
from contend.models import Bus, Gps, Conductor, Ruta


class BusForm(forms.ModelForm):
    serial = forms.CharField(max_length=5,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Serial GPS'}))

    class Meta:
        model = Bus
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patente del vehículo'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo del vehículo'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color del vehículo'}),
            'fechaVencimiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha vencimiento revisión técnica'}),
        }
        exclude = ['empresa', 'estado', 'serialGps']


class EditarBusForm(forms.ModelForm):
    class Meta:
        model = Bus
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patente del vehículo'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo del vehículo'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color del vehículo'}),
            'fechaVencimiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha vencimiento revisión técnica'}),
        }
        exclude = ['empresa', 'estado', 'serialGps', 'habilitado']


class SerialGpsForm(forms.ModelForm):
    class Meta:
        model = Gps
        fields = ['serial']


class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del conductor'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido del conductor'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rut del conductor'}),
            'dv': forms.Select(attrs={'class': 'form-control'}),
            'fechaNacimiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de nacimiento del conductor'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección del conductor'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono del conductor'}),
            'fechaVencimiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de vencimiento de lincencia de conducir'}),
        }
        exclude = ['habilitado', 'empresa']


class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la ruta'}),
        }
        exclude = ['habilitado']
