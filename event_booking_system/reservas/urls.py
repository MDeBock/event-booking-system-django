from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('crear/<int:salon_id>/', views.crear_reserva, name='crear_reserva'),
    # NUEVA RUTA PARA PAGOS (SEÑAS O TOTALES)
    path('pagar/<int:reserva_id>/', views.pagar_reserva, name='pagar_reserva'),
]