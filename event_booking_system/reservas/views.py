from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalogo.models import Salon, TipoEvento, Adicional
from .models import Reserva, ReservaAdicional

# Truco temporal: redirige al admin si no hay sesión iniciada
@login_required(login_url='/admin/login/') 
def crear_reserva(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    tipos_evento = TipoEvento.objects.all()
    # ACÁ ESTÁ LA MAGIA: Solo traemos los adicionales permitidos para ESTE salón
    adicionales_permitidos = salon.adicionales_disponibles.all()

    if request.method == 'POST':
        tipo_evento_id = request.POST.get('tipo_evento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        # getlist() captura todos los checkboxes que el usuario tildó
        extras_seleccionados_ids = request.POST.getlist('extras') 

        try:
            tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
            
            # 1. Creamos la reserva base (el save() del modelo que armamos antes va a autocompletar el precio)
            reserva = Reserva.objects.create(
                cliente=request.user,
                salon=salon,
                tipo_evento=tipo_evento,
                fecha_hora_inicio=fecha_inicio,
                fecha_hora_liberacion=fecha_fin,
            )

            # 2. Le adjuntamos los extras seleccionados
            for extra_id in extras_seleccionados_ids:
                adicional = get_object_or_404(Adicional, id=extra_id)
                # El save() del modelo autocompleta el precio de cada extra
                ReservaAdicional.objects.create(reserva=reserva, adicional=adicional)

            messages.success(request, f'¡Reserva para el salón {salon.nombre} creada con éxito!')
            return redirect('home') # Por ahora volvemos al inicio tras reservar

        except Exception as e:
            messages.error(request, f'Ocurrió un error al procesar la reserva: {str(e)}')

    return render(request, 'reservas/crear_reserva.html', {
        'salon': salon,
        'tipos_evento': tipos_evento,
        'adicionales': adicionales_permitidos
    })