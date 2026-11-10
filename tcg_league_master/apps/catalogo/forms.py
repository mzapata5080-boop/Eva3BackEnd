from django import forms
from .models import TorneoTCG


class TorneoTCGForm(forms.ModelForm):
    class Meta:
        model = TorneoTCG
        fields = [
            'codigo', 'nombre', 'franquicia', 'formato', 'fecha_evento', 
            'lugar', 'precio_inscripcion', 'cupos_maximos', 'cupos_disponibles', 
            'estado', 'afiche', 'destacado', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. MTG-CMD-01'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Torneo Major Commander FNM'}),
            'franquicia': forms.Select(attrs={'class': 'form-select'}),
            'formato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Commander / EDH'}),
            'fecha_evento': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Tienda La Ira - Chillán'}),
            'precio_inscripcion': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'cupos_maximos': forms.NumberInput(attrs={'class': 'form-control', 'min': 4}),
            'cupos_disponibles': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'afiche': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', '').upper()
        if len(codigo) < 4:
            raise forms.ValidationError("El código del torneo debe tener al menos 4 caracteres.")
        return codigo

    def clean_cupos_disponibles(self):
        disponibles = self.cleaned_data.get('cupos_disponibles')
        maximos = self.cleaned_data.get('cupos_maximos')
        if disponibles is not None and maximos is not None and disponibles > maximos:
            raise forms.ValidationError("Los cupos disponibles no pueden superar el aforo máximo.")
        return disponibles