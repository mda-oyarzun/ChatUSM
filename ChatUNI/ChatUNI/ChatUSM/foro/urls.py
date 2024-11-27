from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin-panel/usuarios/editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('admin-panel/solicitudes_eliminar_tema/', views.manejar_solicitudes_eliminar_tema, name='manejar_solicitudes_eliminar_tema'),
    path('tema/<int:tema_id>/', views.tema_detalle, name='tema_solicitud'),


    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/profile/', views.perfil, name='perfil'),
    path('accounts/profile/votos_positivos/', views.perfil_votos_si, name='perfil_votos_si'),
    path('accounts/profile/votos_negativos/', views.perfil_votos_no, name='perfil_votos_no'),
    path('accounts/profile/editar/<int:user_id>/', views.perfil_editar, name='perfil_editar'),

    path('buscar/', views.buscar, name='buscar'),

    path('', views.index, name='index'),
    path('acerca_de/', views.about, name='about'),
    path('categorias/', views.categorias, name='categorias_lista'),
    path('categorias/<str:tipo>/', views.categorias, name='categorias_por_tipo'),

    path('categorias/<str:categoria_tipo>/agregar_tema/', views.crear_tema, name='crear_tema'), 
    path('categorias/<slug:tipo>/<int:tema_id>/', views.detalle_tema, name='detalle_tema'), # CATEGORÍA -> TEMAS
    path('buscar/tema/<int:tema_id>/', views.tema_detalle, name='tema_detalle'), # BUSCADOR -> TEMA
    path('enviar-solicitud-eliminar-tema/<int:tema_id>/', views.enviar_solicitud_eliminar_tema, name='enviar_solicitud_eliminar_tema'),

    path('categorias/<int:tema_id>/agregar_comentario/', views.agregar_comentario, name='agregar_comentario'),
    path('categorias/<str:tipo>/<int:tema_id>/eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),

    path('comentario/si/<int:comentario_id>/', views.comentario_si, name='comentario_si'),
    path('comentario/no/<int:comentario_id>/', views.comentario_no, name='comentario_no'),
    path('tema/si/<int:tema_id>/', views.tema_si, name='tema_si'),
    path('tema/no/<int:tema_id>/', views.tema_no, name='tema_no'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)