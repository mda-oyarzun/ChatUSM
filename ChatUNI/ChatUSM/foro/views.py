from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Tema, Comentario, SolicitudEliminacionTema, Usuario, TipoUsuario, Sede, Carrera, VotoTema, VotoComentario
from .forms import TemaForm, ComentarioForm, SolicitudEliminacionTemaForm, UsuarioForm
from django.http import HttpResponseBadRequest
from django.db.models import Q, Func, F
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
#from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone

#def login(request):
#    return redirect(LoginView.as_view())

# ADMINISTRADORES
@login_required
def admin_panel(request):
    return render(request, 'foro/admin_panel.html')

from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Usuario, TipoUsuario, Sede, Carrera, Categoria

@login_required
def admin_usuarios(request):
    q = request.GET.get('q', '')
    usuarios = Usuario.objects.filter(
        Q(id__icontains=q) |
        Q(nombre__icontains=q) |
        Q(apellido__icontains=q) |
        Q(email__icontains=q) |
        Q(tipo__nombre__icontains=q) |
        Q(sede__nombre__icontains=q) |
        Q(categoria__nombre__icontains=q)
    ).order_by('nombre', 'apellido')

    cant_tipo = {}
    tipos = TipoUsuario.objects.all()
    sedes = Sede.objects.all()
    carreras = Carrera.objects.all()
    categorias = Categoria.objects.all()

    for tipo in tipos:
        cant_tipo[tipo.nombre] = usuarios.filter(tipo=tipo).count()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('correo')  # Este es el correo electrónico
        password = request.POST.get('contraseña')
        tipo_id = request.POST.get('tipo')
        sede_id = request.POST.get('sede')
        carrera_id = request.POST.get('carrera')
        categoria_id = request.POST.get('categoria')

        # Verifica si el correo electrónico ya existe
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'foro/admin_usuarios.html', {
                'usuarios': usuarios,
                'tipos': tipos,
                'sedes': sedes,
                'carreras': carreras,
                'categorias': categorias,
                'cant_tipo': cant_tipo,
                'error': 'El correo electrónico ya está en uso.'
            })

        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            username=email,  # Asigna el correo electrónico como nombre de usuario
            email=email,
            nombre=nombre,
            apellido=apellido,
            tipo_id=tipo_id,
            sede_id=sede_id,
            carrera_id=carrera_id,
            categoria_id=categoria_id,
        )
        nuevo_usuario.set_password(password)  # Asegúrate de usar set_password para almacenar la contraseña de forma segura
        nuevo_usuario.save()  # Guarda el nuevo usuario en la base de datos

        return redirect('admin_usuarios')  # Redirige a la misma vista para mostrar el nuevo usuario

    return render(request, 'foro/admin_usuarios.html', {
        'usuarios': usuarios,
        'tipos': tipos,
        'sedes': sedes,
        'carreras': carreras,
        'categorias': categorias,
        'cant_tipo': cant_tipo,
        'q': q
    })

@login_required
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    tipos = TipoUsuario.objects.all()
    sedes = Sede.objects.all()
    carreras = Carrera.objects.all()
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.apellido = request.POST.get('apellido')
        usuario.email = request.POST.get('correo')
        usuario.password = request.POST.get('contraseña')
        usuario.tipo_id = request.POST.get('tipo')
        usuario.sede_id = request.POST.get('sede')
        usuario.carrera_id = request.POST.get('carrera')
        usuario.categoria_id = request.POST.get('categoria')
        usuario.save()
        return redirect('admin_usuarios')
    
    return render(request, 'foro/admin_editar_usuario.html', {
        'usuario': usuario,
        'tipos': tipos,
        'sedes': sedes,
        'carreras': carreras,
        'categorias': categorias,
    })

@login_required
def perfil_editar(request, user_id):
    user = get_object_or_404(Usuario, id=user_id)
    sedes = Sede.objects.all()
    carreras = Carrera.objects.all()

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            # Si se proporciona una nueva contraseña, hashearla
            new_password = form.cleaned_data.get('contraseña')
            if new_password:
                user.password = make_password(new_password)  # Hash de la nueva contraseña
            user.sede_id = form.cleaned_data.get('sede')
            user.carrera_id = form.cleaned_data.get('carrera')
            user.save()
            messages.success(request, 'Perfil actualizado.')
            return redirect('admin_usuarios')
        else:
            messages.error(request, 'A ocurrido un error. Por favor revisa el formulario.')

    else:
        form = UsuarioForm(instance=user)

    return render(request, 'foro/perfil_editar.html', {
        'form': form,
        'sedes': sedes,
        'carreras': carreras,
    })

@login_required
def perfil(request):
    user = request.user
    temas_creados = Tema.objects.filter(autor=user).order_by('-fecha_creacion')
    comentarios_creados = Comentario.objects.filter(autor=user).order_by('-fecha_creacion')
    
    cant_temas = temas_creados.count()
    cant_comentarios = comentarios_creados.count()
    
    context = {
        'user': user,
        'temas_creados': temas_creados,
        'comentarios_creados': comentarios_creados,
        'cant_temas': cant_temas,
        'cant_comentarios': cant_comentarios
    }
    return render(request, 'perfil.html', context)

@login_required
def perfil_votos_si(request):
    user = request.user
    # Obtener los votos del usuario para los temas
    votos_tema_si = VotoTema.objects.filter(usuario=user, voto=True).values_list('tema', flat=True)
    votos_comentario_si = VotoComentario.objects.filter(usuario=user, voto=True).values_list('comentario', flat=True)

    # Filtrar los temas según los votos
    temas_votados_si = Tema.objects.filter(id__in=votos_tema_si)
    comentarios_votados_si = Comentario.objects.filter(id__in=votos_comentario_si)

    cant_temas_si = temas_votados_si.count()
    cant_comentarios_si = comentarios_votados_si.count()

    context = {
        'user': user,
        'temas_votados_si': temas_votados_si,
        'comentarios_votados_si': comentarios_votados_si,
        'cant_temas_si': cant_temas_si,
        'cant_comentarios_si': cant_comentarios_si
    }
    return render(request, 'perfil_votos_si.html', context)

@login_required
def perfil_votos_no(request):
    user = request.user
    # Obtener los votos del usuario para los temas
    votos_tema_no = VotoTema.objects.filter(usuario=user, voto=False).values_list('tema', flat=True)
    votos_comentario_no = VotoComentario.objects.filter(usuario=user, voto=False).values_list('comentario', flat=True)

    # Filtrar los temas según los votos
    temas_votados_no = Tema.objects.filter(id__in=votos_tema_no)
    comentarios_votados_no = Comentario.objects.filter(id__in=votos_comentario_no)

    cant_temas_no = temas_votados_no.count()
    cant_comentarios_no = comentarios_votados_no.count()

    context = {
        'user': user,
        'temas_votados_no': temas_votados_no,
        'comentarios_votados_no': comentarios_votados_no,
        'cant_temas_no': cant_temas_no,
        'cant_comentarios_no': cant_comentarios_no
    }
    return render(request, 'perfil_votos_no.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def index(request):
    categorias = Categoria.objects.all()
    return render(request, 'foro/index.html', {'categorias': categorias})

def about(request):
    return render(request, 'foro/about.html')

def categorias(request, tipo):
    categoria = Categoria.objects.get(tipo=tipo)
    categorias = Categoria.objects.all().order_by('nombre')
    temas = Tema.objects.filter(categoria=categoria).order_by('-fecha_creacion')
    return render(request, 'foro/categorias.html', {'temas': temas, 'categoria': categoria, 'categorias': categorias})

def crear_tema(request, categoria_tipo):
    try:
        categoria = Categoria.objects.get(tipo=categoria_tipo)
    except Categoria.DoesNotExist:

        return HttpResponseBadRequest('No se encontró la categoría')
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            tema = form.save(commit=False)
            tema.autor_id = request.user.id
            tema.categoria_id = categoria.id
            tema.save()
            return redirect('categorias_por_tipo', tipo=categoria_tipo)
    else:
        form = TemaForm()
    return render(request, 'foro/agregar_tema.html', {'form': form, 'categoria_tipo': categoria_tipo})


def detalle_tema(request, tipo, tema_id): # CONVERSACIÓN
    tema = get_object_or_404(Tema, pk=tema_id)
    categoria = tema.categoria
    comentarios = tema.comentarios.all()

    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            Comentario.objects.create(tema=tema, autor=request.user, contenido=contenido)
            return redirect('detalle_tema', tema_id=tema.id)

    return render(request, 'foro/detalle_tema.html', {'categoria': categoria, 'tema': tema, 'comentarios': comentarios})

def buscar(request): # BUSCAR
    q = request.GET.get('q', '')
    temas = Tema.objects.filter(titulo__icontains=q).annotate(sort_key=Func(F('titulo'), function='LOWER')).order_by('sort_key')
    categorias = Categoria.objects.filter(nombre__icontains=q).annotate(sort_key=Func(F('nombre'), function='LOWER')).order_by('sort_key')
    return render(request, 'foro/buscar.html', {'temas': temas, 'categorias': categorias, 'q': q})

def tema_detalle(request, tema_id): # BUSCADOR
    tema = get_object_or_404(Tema, id=tema_id)
    categoria = tema.categoria
    comentarios = Comentario.objects.filter(tema=tema)
    return render(request, 'foro/detalle_tema.html', {'categoria': categoria, 'tema': tema, 'comentarios': comentarios})

def enviar_solicitud_eliminar_tema(request, tema_id):
    tema = get_object_or_404(Tema, pk=tema_id)
    if request.method == 'POST':
        form = SolicitudEliminacionTemaForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.tema = tema
            solicitud.usuario = request.user
            solicitud.estado = 'pendiente'
            solicitud.save()
            return redirect('detalle_tema', tipo=tema.categoria.tipo, tema_id=tema.id) 
    else:
        form = SolicitudEliminacionTemaForm()
    return render(request, 'foro/eliminar_tema.html', {'tema': tema, 'form': form})

def manejar_solicitudes_eliminar_tema(request):
    solicitudes = SolicitudEliminacionTema.objects.filter(estado='pendiente')
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        solicitud = get_object_or_404(SolicitudEliminacionTema, id=solicitud_id)
        password = request.POST.get('password')

        if request.user.check_password(password):
            if request.POST.get('accion') == 'aceptar':
                solicitud.estado = 'aceptada'
                solicitud.save()
                tema = solicitud.tema
                tema.delete()
            elif request.POST.get('accion') == 'rechazar':
                justificacion = request.POST.get('justificacion')
                solicitud.estado = 'rechazada'
                solicitud.respuesta = justificacion
                solicitud.save()
        else:
            error = "La contraseña es incorrecta."
            return render(request, 'foro/admin_solicitudes_eliminar_tema.html', {'solicitudes': solicitudes, 'error': error})

    return render(request, 'foro/admin_solicitudes_eliminar_tema.html', {'solicitudes': solicitudes})

def agregar_comentario(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.tema = tema
            comentario.autor = request.user
            
            
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comentario.parent_id = parent_id 
            
            comentario.save()
            return redirect('detalle_tema', tipo=tema.categoria.tipo, tema_id=tema_id)
    else:
        form = ComentarioForm()
    
    return render(request, 'detalle_tema.html', {'form': form, 'tema': tema})

def eliminar_comentario(request, tipo, tema_id, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    if request.method == 'POST':
        comentario.delete()
        return redirect('detalle_tema', tipo=tipo, tema_id=tema_id)
    return render(request, 'foro/eliminar_comentario.html', {'comentario': comentario})

def comentario_si(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    # Verifica si el usuario ya ha votado
    voto_existente = VotoComentario.objects.filter(usuario=request.user, comentario=comentario).first()
    
    if voto_existente:
        # Si el usuario ya ha votado, actualiza su voto
        if voto_existente.voto:  # Si ya votó "Sí", no hacemos nada
            pass
        else:  # Si votó "No", actualizamos a "Sí"
            voto_existente.voto = True
            voto_existente.save()
            comentario.si += 1
            comentario.no -= 1  # Decrementamos el contador de "No"
            comentario.save()
    else:
        # Si no ha votado, crea un nuevo voto
        VotoComentario.objects.create(usuario=request.user, comentario=comentario, voto=True)
        comentario.si += 1
        comentario.save()

    return redirect('detalle_tema', tipo=comentario.tema.categoria.tipo, tema_id=comentario.tema.id)

def comentario_no(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    # Verifica si el usuario ya ha votado
    voto_existente = VotoComentario.objects.filter(usuario=request.user, comentario=comentario).first()
    
    if voto_existente:
        # Si el usuario ya ha votado, actualiza su voto
        if not voto_existente.voto:  # Si ya votó "No", no hacemos nada
            pass
        else:  # Si votó "Sí", actualizamos a "No"
            voto_existente.voto = False
            voto_existente.save()
            comentario.no += 1
            comentario.si -= 1  # Decrementamos el contador de "Sí"
            comentario.save()
    else:
        # Si no ha votado, crea un nuevo voto
        VotoComentario.objects.create(usuario=request.user, comentario=comentario, voto=False)
        comentario.no += 1
        comentario.save()

    return redirect('detalle_tema', tipo=comentario.tema.categoria.tipo, tema_id=comentario.tema.id)

def tema_si(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)

    # Verifica si el usuario ya ha votado
    voto_existente = VotoTema.objects.filter(usuario=request.user, tema=tema).first()
    
    if voto_existente:
        # Si el usuario ya ha votado, actualiza su voto
        if voto_existente.voto:  # Si ya votó "Sí", no hacemos nada
            pass
        else:  # Si votó "No", actualizamos a "Sí"
            voto_existente.voto = True
            voto_existente.save()
            tema.si += 1
            tema.no -= 1  
            tema.save()
    else:
        # Si no ha votado, crea un nuevo voto
        VotoTema.objects.create(usuario=request.user, tema=tema, voto=True)
        tema.si += 1
        tema.save()

    return redirect('detalle_tema', tipo=tema.categoria.tipo, tema_id=tema.id)

def tema_no(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)

    # Verifica si el usuario ya ha votado
    voto_existente = VotoTema.objects.filter(usuario=request.user, tema=tema).first()
    
    if voto_existente:
        # Si el usuario ya ha votado, actualiza su voto
        if not voto_existente.voto:  # Si ya votó "No", no hacemos nada
            pass
        else:  # Si votó "Sí", actualizamos a "No"
            voto_existente.voto = False
            voto_existente.save()
            tema.no += 1
            tema.si -= 1  # Decrementamos el contador de "Sí"
            tema.save()
    else:
        # Si no ha votado, crea un nuevo voto
        VotoTema.objects.create(usuario=request.user, tema=tema, voto=False)
        tema.no += 1
        tema.save()

    return redirect('detalle_tema', tipo=tema.categoria.tipo, tema_id=tema.id)