from django import forms
from contend.models import Bus, Gps, Conductor

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
        exclude = ['habilitado']
