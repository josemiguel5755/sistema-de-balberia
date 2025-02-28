from django.urls import path
from . import views
from django.contrib.staticfiles.views import serve

urlpatterns = [
    
     path("", views.index, name="index"),
     path("ver_citas", views.ver_citas, name="ver_citas"),
     path("guardar_cita", views.guardar_cita, name="guardar_cita"),
     path("adminis", views.adminis, name="adminis"),
     path('cambiar_estado/', views.cambiar_estado, name='cambiar_estado'),
     path('eliminar-cita/', views.eliminar_cita, name='eliminar_cita'),
     # path('editar-cita/', views.editar_cita, name='editar_cita'),
     path('editar_cliente/', views.editar_cliente, name='editar_cliente'),
     path('horario', views.horario, name='horario'),
     path('guardar_horario/', views.guardar_horario, name='guardar_horario'),
     path("obtener_horarios/", views.obtener_horarios, name="obtener_horarios"),
     path("eliminar_horario/", views.eliminar_horario, name="eliminar_horario"),
     path('horas/', views.vista_horas, name='vista_horas'),
     path('citas', views.citas, name='citas'),
     path('iniciosesion', views.iniciosesion, name='iniciosesion'),
     #path('cancelar-cita/', views.cancelar_cita, name='cancelar_cita'),
     path('manifest.json', serve, {'path': 'agenda/manifest.json'}),
     path('sw.js', serve, {'path': 'agenda/sw.js'}),
     path('cancelar_cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
]
