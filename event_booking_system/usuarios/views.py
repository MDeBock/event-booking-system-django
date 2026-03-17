from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum

from .forms import RegistroClienteForm
from reservas.models import Reserva

@login_required(login_url='usuarios:login')
def panel_cliente(request):
    # REDIRECCIÓN AUTOMÁTICA: Si es empleado, va al panel gerencial
    if request.user.is_staff:
        return redirect('usuarios:panel_gerente')

    # Si es cliente normal, ve sus reservas
    reservas = request.user.reservas.all().order_by('-fecha_hora_inicio')
    return render(request, 'usuarios/panel.html', {
        'reservas': reservas
    })

def registro(request):
    if request.user.is_authenticated:
        return redirect('usuarios:panel')

    if request.method == 'POST':
        form = RegistroClienteForm(request.POST) 
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f'¡Bienvenido {usuario.username}! Tu cuenta ha sido creada exitosamente.')
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('usuarios:panel')
    else:
        form = RegistroClienteForm() 

    return render(request, 'usuarios/registro.html', {'form': form})

@login_required(login_url='usuarios:login')
def panel_gerente(request):
    if not request.user.is_staff:
        messages.error(request, 'No tenés permisos para ver esta pantalla.')
        return redirect('usuarios:panel')

    es_administrativo = request.user.groups.filter(name='Administrativos').exists() or request.user.is_superuser

    todas_las_reservas = Reserva.objects.all().order_by('-fecha_hora_inicio')
    
    reservas_pendientes = todas_las_reservas.filter(estado='Pendiente').count()
    reservas_confirmadas = todas_las_reservas.filter(estado='Confirmada').count()
    
    recaudacion = 0
    if es_administrativo:
        recaudacion = todas_las_reservas.aggregate(total=Sum('monto_abonado'))['total'] or 0

    return render(request, 'usuarios/panel_gerente.html', {
        'reservas': todas_las_reservas,
        'reservas_pendientes': reservas_pendientes,
        'reservas_confirmadas': reservas_confirmadas,
        'recaudacion': recaudacion,
        'es_administrativo': es_administrativo,
    })