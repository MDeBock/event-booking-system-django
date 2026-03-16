from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from catalogo.models import Salon, TipoEvento, Adicional
from .models import Reserva, ReservaAdicional

def crear_reserva(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    tipos_evento = TipoEvento.objects.all()
    adicionales_permitidos = salon.adicionales_disponibles.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Debés iniciar sesión para confirmar una reserva.')
            return redirect('usuarios:login')

        tipo_evento_id = request.POST.get('tipo_evento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        extras_seleccionados_ids = request.POST.getlist('extras') 

        try:
            tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
            
            reserva = Reserva.objects.create(
                cliente=request.user,
                salon=salon,
                tipo_evento=tipo_evento,
                fecha_hora_inicio=fecha_inicio,
                fecha_hora_liberacion=fecha_fin,
            )

            for extra_id in extras_seleccionados_ids:
                adicional = get_object_or_404(Adicional, id=extra_id)
                ReservaAdicional.objects.create(reserva=reserva, adicional=adicional)

            messages.success(request, f'¡Reserva para el salón {salon.nombre} creada con éxito!')
            return redirect('usuarios:panel') 

        except Exception as e:
            messages.error(request, f'Ocurrió un error al procesar la reserva: {str(e)}')

    return render(request, 'reservas/crear_reserva.html', {
        'salon': salon,
        'tipos_evento': tipos_evento,
        'adicionales': adicionales_permitidos
    })

@login_required(login_url='usuarios:login')
def pagar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)

    # 1. ¿Cuánto valía la fiesta originalmente?
    precio_total_original = reserva.monto_abonado + reserva.saldo_a_pagar
    
    if precio_total_original <= 0 or reserva.saldo_a_pagar <= 0:
        messages.info(request, 'Esta reserva ya se encuentra totalmente abonada.')
        return redirect('usuarios:panel')

    # 2. ¿Qué porcentaje ya tiene asegurado el cliente con su plata?
    porcentaje_pagado = reserva.monto_abonado / precio_total_original
    porcentaje_restante = Decimal('1.0') - porcentaje_pagado

    # 3. ¿Cuánto vale la fiesta HOY con los precios actualizados de la base de datos?
    precio_salon_hoy = reserva.salon.precio_base
    
    # CORRECCIÓN ACÁ: Consultamos la tabla ReservaAdicional directamente para evitar el AttributeError
    extras_de_esta_reserva = ReservaAdicional.objects.filter(reserva=reserva)
    precio_extras_hoy = sum(item.adicional.precio_actual for item in extras_de_esta_reserva)
    
    presupuesto_actualizado = precio_salon_hoy + precio_extras_hoy

    # 4. Lo que debe es estrictamente el % restante multiplicado por el precio de HOY
    saldo_real_pendiente = presupuesto_actualizado * porcentaje_restante

    # 5. La diferencia para que la contabilidad cuadre perfecta (el beneficio del cliente)
    descuento_pago_anticipado = presupuesto_actualizado - saldo_real_pendiente - reserva.monto_abonado
    if descuento_pago_anticipado < 0:
        descuento_pago_anticipado = Decimal('0')

    sena_sugerida = saldo_real_pendiente * Decimal('0.30')

    if request.method == 'POST':
        try:
            monto_ingresado = Decimal(request.POST.get('monto_pago', '0'))
            
            if monto_ingresado <= 0:
                messages.error(request, 'El monto a abonar debe ser mayor a cero.')
            elif monto_ingresado > saldo_real_pendiente:
                messages.error(request, 'El monto no puede superar el saldo pendiente.')
            else:
                reserva.monto_abonado += monto_ingresado
                if reserva.monto_abonado > 0:
                    reserva.estado = 'Confirmada'
                reserva.save()
                messages.success(request, f'¡Pago de ${monto_ingresado|floatformat:0} procesado con éxito!')
                return redirect('usuarios:panel')
        except Exception as e:
            messages.error(request, 'Por favor ingrese un monto válido.')

    return render(request, 'reservas/pagar_reserva.html', {
        'reserva': reserva,
        'presupuesto_actualizado': presupuesto_actualizado,
        'saldo_real_pendiente': saldo_real_pendiente,
        'descuento_pago_anticipado': descuento_pago_anticipado,
        'sena_sugerida': sena_sugerida
    })