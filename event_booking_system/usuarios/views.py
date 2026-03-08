from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='usuarios:login')
def panel_cliente(request):
    # Traemos todas las reservas del cliente logueado, de la más reciente a la más antigua
    reservas = request.user.reservas.all().order_by('-fecha_hora_inicio')
    
    return render(request, 'usuarios/panel.html', {
        'reservas': reservas
    })