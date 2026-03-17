from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Salon
from .forms import SalonForm

# ==========================================
# VISTA 1: EL CATÁLOGO PÚBLICO
# ==========================================
def lista_salones(request):
    salones = Salon.objects.all()
    return render(request, 'catalogo/lista_salones.html', {
        'salones': salones
    })

# ==========================================
# VISTA 2: PROMOCIONES (PRÓXIMAMENTE)
# ==========================================
def promociones(request):
    return render(request, 'catalogo/promos.html')

# ==========================================
# VISTA 3: ALTA DE SALONES (SOLO STAFF)
# ==========================================
@login_required(login_url='usuarios:login')
def crear_salon(request):
    if not request.user.is_staff:
        messages.error(request, 'No tenés permisos para gestionar salones.')
        return redirect('catalogo:lista_salones')

    if request.method == 'POST':
        form = SalonForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_salon = form.save()
            messages.success(request, f'¡El salón "{nuevo_salon.nombre}" se publicó con éxito!')
            return redirect('usuarios:panel_gerente')
        else:
            messages.error(request, 'Por favor, corregí los errores en el formulario.')
    else:
        form = SalonForm()

    return render(request, 'catalogo/crear_salon.html', {'form': form})