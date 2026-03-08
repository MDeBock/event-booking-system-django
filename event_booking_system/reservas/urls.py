from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('crear/<int:salon_id>/', views.crear_reserva, name='crear_reserva'),
]