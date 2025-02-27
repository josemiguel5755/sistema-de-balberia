from django.shortcuts import render, redirect
from .forms import ClienteForm
from .models import Cliente
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db import transaction
from datetime import datetime, time
from django.views.decorators.http import require_http_methods
from django.db.models import Max
from .models import HorarioNoDisponible
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404
import hashlib
from django.contrib.auth.decorators import login_required



@csrf_exempt
@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = ClienteForm(data)
            
            if form.is_valid():
                cita = form.save()
                return JsonResponse({'success': True, 'mensaje': 'Cita creada exitosamente'})
            else:
                return JsonResponse({'success': False, 'error': form.errors}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
    
    # Obtener las citas ordenadas por fecha y hora
    citas = Cliente.objects.all().order_by('fecha', 'hora')

    # Obtener las fechas y horas del modelo HorarioNoDisponible
    horas_no_disponibles = HorarioNoDisponible.objects.exclude(hora__isnull=True).values_list('hora', flat=True)
    fechas_no_disponibles = HorarioNoDisponible.objects.exclude(fecha__isnull=True).values_list('fecha', flat=True)
    
    return render(request, 'agenda/index.html', {
        'citas': citas,
        'horas_no_disponibles': horas_no_disponibles,
        'fechas_no_disponibles': list(fechas_no_disponibles),  # Convertir a lista para serializar en JSON
    })



# @csrf_exempt
# def guardar_cita(request):
#     """Guardar nueva cita"""
#     if request.method == 'POST':
#         try:
#             # Cargar los datos del cuerpo de la solicitud
#             data = json.loads(request.body)

#             # Asegurarse de que los datos requeridos están presentes
#             campos_requeridos = ['nombre', 'telefono', 'fecha', 'hora']
#             for campo in campos_requeridos:
#                 if campo not in data or not data[campo]:
#                     return JsonResponse({'success': False, 'error': f'El campo {campo} es obligatorio.'}, status=400)

#             fecha = data['fecha']
#             hora = data['hora']

#             # Validar si la fecha y hora ya están ocupadas
#             if Cliente.objects.filter(fecha=fecha, hora=hora).exists():
#                 return JsonResponse({
#                     'success': False,
#                     'error': 'Esta hora ya está agendada por otro cliente. Por favor, elija otra.'
#                 }, status=400)

#             # Calcular el próximo turno basado en el último turno registrado
#             ultimo_turno = Cliente.objects.aggregate(max_turno=Max('turno'))['max_turno'] or 0
#             nuevo_turno = ultimo_turno + 1

#             # Crear la cita con el turno asignado
#             form = ClienteForm(data)
#             if form.is_valid():
#                 cita = form.save(commit=False)  # No guarda aún en la base de datos
#                 cita.turno = nuevo_turno  # Asignar el turno generado
#                 cita.save()  # Ahora sí guarda la cita en la base de datos

#                 return JsonResponse({'success': True, 'mensaje': 'Cita creada exitosamente', 'turno': nuevo_turno})
#             else:
#                 # Si el formulario no es válido, devolver los errores
#                 return JsonResponse({'success': False, 'error': form.errors}, status=400)

#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=500)

#     # Si no es una solicitud POST
#     return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)





@csrf_exempt 
def ver_citas(request):
    # Sort by fecha first, then by hora
    citas = Cliente.objects.values('nombre', 'telefono', 'fecha', 'hora', 'estado').order_by('fecha', 'hora')
    
    # Convert to list and sort with a custom key
    citas_list = [
        {
            'turno': idx + 1,
            'nombre': cita['nombre'],
            'telefono': cita['telefono'],
            'fecha': cita['fecha'].strftime('%Y-%m-%d'),
            'hora': cita['hora'].strftime('%I:%M %p'),
            'estado': cita['estado']
        }
        for idx, cita in enumerate(sorted(citas, key=lambda x: (x['fecha'], x['hora'])))
    ]
    
    return JsonResponse(citas_list, safe=False)




# def modificar_turno(request):
#     """Cambia el turno de una cita y reorganiza los turnos según sea necesario."""
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         cliente_id = data.get('id')
#         nuevo_turno = data.get('turno')
#         fecha = data.get('fecha')

#         try:
#             with transaction.atomic():
#                 cliente = Cliente.objects.get(id=cliente_id)
#                 turno_anterior = cliente.turno

#                 if turno_anterior != nuevo_turno:
#                     if turno_anterior < nuevo_turno:
#                         # Turno desplazado hacia arriba
#                         Cliente.objects.filter(
#                             fecha=fecha,
#                             turno__gt=turno_anterior,
#                             turno__lte=nuevo_turno
#                         ).update(turno=F('turno') - 1)
#                     else:
#                         # Turno desplazado hacia abajo
#                         Cliente.objects.filter(
#                             fecha=fecha,
#                             turno__gte=nuevo_turno,
#                             turno__lt=turno_anterior
#                         ).update(turno=F('turno') + 1)

#                     cliente.turno = nuevo_turno
#                     cliente.save()

#             return JsonResponse({'success': True, 'message': 'Turno actualizado correctamente.'})
#         except Cliente.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Cliente no encontrado.'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})




def obtener_horarios(request):
    if request.method == "GET":
        horarios = HorarioNoDisponible.objects.all()
        data = {
            "horas": [h.hora for h in horarios if h.hora],
            "fechas": [h.fecha for h in horarios if h.fecha],
        }
        return JsonResponse(data)
    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)




@csrf_exempt
def eliminar_horario(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tipo = data.get("tipo")  # "hora" o "fecha"
            valor = data.get("valor")  # Hora o Fecha a eliminar

            if tipo == "hora":
                HorarioNoDisponible.objects.filter(hora=valor).delete()
            elif tipo == "fecha":
                HorarioNoDisponible.objects.filter(fecha=valor).delete()

            return JsonResponse({"mensaje": "Horario eliminado correctamente", "estado": "exito"})
        except Exception as e:
            return JsonResponse({"mensaje": "Error al eliminar el horario", "estado": "error", "error": str(e)}, status=400)
    return JsonResponse({"mensaje": "Método no permitido"}, status=405)



def vista_horas(request):
    horas = HorarioNoDisponible.objects.exclude(hora__isnull=True).values_list('hora', flat=True)
    context = {
        'horas': horas,
    }
    return render(request, 'index.html', context)


@csrf_exempt
def eliminar_cita(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_cita = data.get('id')
        try:
            # First, get the cita to be deleted
            cita = Cliente.objects.get(id=id_cita)
            
            # Delete the cita
            cita.delete()
            
            # Reorder turns without saving to avoid unique constraint
            clientes = Cliente.objects.all().order_by('fecha', 'hora')
            for index, cliente in enumerate(clientes, start=1):
                # Use update to bypass the unique constraint
                Cliente.objects.filter(id=cliente.id).update(turno=index)
            
            return JsonResponse({'success': True})
        
        except Cliente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'La cita no existe.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


# parte del administrador
@login_required(login_url='iniciosesion')  # Decorador que redirige a 'iniciosesion' si no está autenticado
def adminis(request):
    # Verificar si es superusuario, si no lo es, redirigir
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('iniciosesion')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Fetch all appointments
        citas = list(Cliente.objects.values(
            'id', 'turno', 'nombre', 'telefono', 'fecha', 'hora', 'estado'
        ))
        
        # Sort appointments by date and time
        citas.sort(key=lambda x: (x['fecha'], x['hora']))
        
        # Reassign turns dynamically based on sorted order
        for idx, cita in enumerate(citas, 1):
            cita['turno'] = idx
        
        # Prepare the list for JSON response
        citas_list = [
            {
                'id': cita['id'],
                'turno': cita['turno'],
                'nombre': cita['nombre'],
                'telefono': cita['telefono'] or '',
                'fecha': cita['fecha'].strftime('%Y-%m-%d'),
                'hora': cita['hora'].strftime('%I:%M %p'),
                'estado': cita['estado'],
            }
            for cita in citas
        ]
        
        return JsonResponse({'success': True, 'citas': citas_list})
    
    return render(request, 'agenda/adminis.html')


@csrf_exempt
def cambiar_estado(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cita_id = data.get('id')
        nuevo_estado = data.get('estado')
        try:
            cita = Cliente.objects.get(id=cita_id)
            cita.estado = nuevo_estado
            cita.save()
            return JsonResponse({'success': True})
        except Cliente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cita no encontrada'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})





@csrf_exempt
def editar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            with transaction.atomic():
                # Obtener el cliente existente
                cliente = Cliente.objects.get(id=data['id'])
                
                # Almacenar la fecha original
                fecha_original = cliente.fecha
                
                # Convertir fecha
                nueva_fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
                
                # Convertir hora (manejar formatos 24h y 12h)
                hora_str = data['hora']
                try:
                    # Intentar parsear como HH:MM
                    nueva_hora = datetime.strptime(hora_str, '%H:%M').time()
                except ValueError:
                    try:
                        # Intentar parsear como formato 12h AM/PM
                        nueva_hora = datetime.strptime(hora_str, '%I:%M %p').time()
                    except ValueError:
                        # Si falla, usar la hora actual
                        nueva_hora = time(hour=int(hora_str.split(':')[0]), 
                                          minute=int(hora_str.split(':')[1][:2]))
                
                # Actualizar los campos
                cliente.fecha = nueva_fecha
                cliente.hora = nueva_hora
                cliente.turno = int(data['turno'])
                
                # Guardar los cambios
                cliente.save()
                
                # Si la fecha cambió, reordenar ambas fechas
                if fecha_original != cliente.fecha:
                    Cliente.reordenar_turnos_por_fecha(fecha_original)
                    Cliente.reordenar_turnos_por_fecha(cliente.fecha)
            
            return JsonResponse({
                'success': True,
                'mensaje': 'Cliente actualizado correctamente'
            })
            
        except Cliente.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Cliente no encontrado'
            })
        except Exception as e:
            print(f"Error al editar cliente: {str(e)}")  # Para debugging
            return JsonResponse({
                'success': False,
                'error': f'Error al actualizar: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })



def horario(request):
    if request.method == "POST":
        if 'hora' in request.POST:
            hora = request.POST.get('hora')
            HorarioNoDisponible.objects.create(hora=hora)
        elif 'fecha' in request.POST:
            fecha = request.POST.get('fecha')
            HorarioNoDisponible.objects.create(fecha=fecha)
        return redirect('horario')

    horarios_no_disponibles = HorarioNoDisponible.objects.all().order_by('hora')  # Ordenar por la hora
    return render(request, 'agenda/horario.html', {'horarios': horarios_no_disponibles})





@csrf_exempt  # Permite solicitudes sin token CSRF para pruebas
def guardar_horario(request):
    if request.method == "POST":
        try:
            # Leer datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)
            tipo = data.get('tipo')  # 'hora' o 'fecha'
            valor = data.get('valor')

            if tipo == "hora":
                HorarioNoDisponible.objects.create(hora=valor)
            elif tipo == "fecha":
                HorarioNoDisponible.objects.create(fecha=valor)
            else:
                return JsonResponse({'mensaje': 'Tipo no válido', 'estado': 'error'}, status=400)

            return JsonResponse({'mensaje': 'Guardado exitosamente', 'estado': 'exito'}, status=201)
        except Exception as e:
            return JsonResponse({'mensaje': f'Error: {str(e)}', 'estado': 'error'}, status=500)
    return JsonResponse({'mensaje': 'Método no permitido', 'estado': 'error'}, status=405)





@require_http_methods(["GET"])
def citas(request):
    token = request.GET.get('token', '')

    # Obtener citas ordenadas por fecha y hora
    citas = Cliente.objects.values(
        'id', 'nombre', 'telefono', 'fecha', 'hora', 'estado', 'token'
    ).order_by('fecha', 'hora')

    # Asignar turnos en orden secuencial
    citas_list = [
        {
            'id': cita['id'],
            'turno': i + 1,  # Asignar turno de forma continua
            'nombre': cita['nombre'],
            'telefono': cita['telefono'],
            'fecha': cita['fecha'].strftime('%Y-%m-%d'),
            'hora': cita['hora'].strftime('%I:%M %p'),
            'estado': cita['estado'],
            'can_cancel': cita['token'] == token
        }
        for i, cita in enumerate(citas)
    ]

    return render(request, 'agenda/citas.html', {
        'citas': citas_list,
        'current_token': token
    })


@csrf_exempt
def guardar_cita(request):
    """Guardar nueva cita"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validar campos requeridos
            campos_requeridos = ['nombre', 'telefono', 'fecha', 'hora']
            for campo in campos_requeridos:
                if campo not in data or not data[campo]:
                    return JsonResponse({'success': False, 'error': f'El campo {campo} es obligatorio.'}, status=400)

            fecha = data['fecha']
            hora = data['hora']

            # Validar si la fecha y hora ya están ocupadas
            if Cliente.objects.filter(fecha=fecha, hora=hora).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Esta hora ya está agendada por otro cliente. Por favor, elija otra.'
                }, status=400)

            # Calcular el próximo turno
            ultimo_turno = Cliente.objects.aggregate(max_turno=Max('turno'))['max_turno'] or 0
            nuevo_turno = ultimo_turno + 1

            # Crear la nueva cita
            nueva_cita = Cliente(
                nombre=data['nombre'],
                telefono=data['telefono'],
                fecha=fecha,
                hora=hora,
                turno=nuevo_turno,
                estado='Pendiente'
            )
            nueva_cita.save()  # Esto generará automáticamente el token

            return JsonResponse({
                'success': True,
                'mensaje': 'Cita creada exitosamente',
                'turno': nuevo_turno,
                'token': nueva_cita.token,
                'redirect_url': f'/citas/?token={nueva_cita.token}'
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@csrf_exempt
def cancelar_cita(request, cita_id):
    token = request.GET.get('token', '')
    device_id = request.GET.get('device_id', '')
    cita = get_object_or_404(Cliente, id=cita_id)
    
    # Verificar si coincide el token
    if cita.token != token:
        return JsonResponse({'error': 'No tienes permiso para cancelar esta cita'}, status=403)
    
    # Verificar adicionalmente si el device_id coincide
    if cita.device_id and cita.device_id != device_id:
        return JsonResponse({'error': 'Esta cita fue creada desde otro dispositivo'}, status=403)
    
    cita.delete()
    return JsonResponse({'message': 'Cita cancelada correctamente'})


def iniciosesion(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated and request.user.is_superuser:
        # Si ya está autenticado y es superusuario, redirigir directamente a adminis
        return redirect("adminis")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            
            # Establecer una cookie de sesión más duradera si el usuario marca "recordarme"
            # (necesitarás agregar esta casilla en tu formulario HTML)
            if request.POST.get("remember_me", False):
                # Configurar que la sesión dure 30 días en lugar del valor predeterminado
                request.session.set_expiry(2592000)  # 30 días en segundos
            
            return redirect("adminis")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "agenda/iniciosesion.html")