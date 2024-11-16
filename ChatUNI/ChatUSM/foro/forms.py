from django import forms
from .models import Tema, Comentario, SolicitudEliminacionTema, Usuario

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ('titulo', 'contenido')

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('contenido',)

class SolicitudEliminacionTemaForm(forms.ModelForm):
    class Meta:
        model = SolicitudEliminacionTema
        fields = ('motivo',)

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['sede', 'carrera', 'password']

    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('pasword')
        if not contraseña:
            return None
        return contraseña