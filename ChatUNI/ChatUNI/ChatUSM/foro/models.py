from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Sede(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Carrera(models.Model):
    nombre = models.CharField(max_length=225, unique=True)
    # años = models.CharField(max_length=1, default='')
   
    def __str__(self):
        return self.nombre


class Categoria(models.Model): # FORO
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.nombre

    
from django.contrib.auth.models import AbstractUser, Group, Permission

class Usuario(AbstractUser ):
    username = models.EmailField(unique=True, null=True, blank=True) 
    nombre = models.CharField(max_length=50, default='Nombre')
    apellido = models.CharField(max_length=100, default='ApellidoPaterno ApellidoMaterno')
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, null=True, blank=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, null=True, blank=True)     
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Tema(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    categoria = models.ForeignKey(Categoria, related_name='temas', on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    anonimo = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    si = models.PositiveIntegerField(default=0)
    no = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.titulo

class SolicitudEliminacionTema(models.Model):
    tema = models.ForeignKey('Tema', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=[
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada')
    ])
    motivo = models.TextField() 
    respuesta = models.TextField(blank=True, null=True) 

class Comentario(models.Model):
    tema = models.ForeignKey('Tema', related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='respuestas', on_delete=models.CASCADE)
    si = models.PositiveIntegerField(default=0)
    no = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return f'Comentario de {self.autor} en {self.tema}'

class VotoTema(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    voto = models.BooleanField()

    class Meta:
        unique_together = ('usuario', 'tema')  # Un usuario solo puede votar una vez por tema

class VotoComentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE)
    voto = models.BooleanField()

    class Meta:
        unique_together = ('usuario', 'comentario')  # Un usuario solo puede votar una vez por comentario