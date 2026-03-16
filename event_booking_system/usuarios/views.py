from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
# Importamos el nuevo formulario que acabamos de crear
from .forms import RegistroClienteForm 

@login_required(login_url='usuarios:login')
def panel_cliente(request):
    reservas = request.user.reservas.all().order_by('-fecha_hora_inicio')
    return render(request, 'usuarios/panel.html', {
        'reservas': reservas
    })

def registro(request):
    # Si el usuario ya está logueado, lo pateamos a su panel
    if request.user.is_authenticated:
        return redirect('usuarios:panel')

    if request.method == 'POST':
        # Usamos TU formulario personalizado
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
        # Usamos TU formulario personalizado
        form = RegistroClienteForm() 

    return render(request, 'usuarios/registro.html', {'form': form})