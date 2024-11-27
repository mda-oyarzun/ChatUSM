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
    password = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput, required=False)
    confirmar_password = forms.CharField(label='Confirmar Nueva Contraseña', widget=forms.PasswordInput, required=False)

    class Meta:
        model = Usuario
        fields = ['sede', 'carrera', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirm_password')

        if password and confirmar_password and password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # Establece la nueva contraseña
        if commit:
            user.save()
        return user