from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Rutas de Autenticación
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    # Usamos next_page='/' para que al salir los mande a la página principal
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    # Rutas del Cliente Normal
    path('registro/', views.registro, name='registro'),
    path('panel/', views.panel_cliente, name='panel'),
    
    # NUEVA RUTA: El Dashboard del Staff/Gerencia
    path('dashboard/', views.panel_gerente, name='panel_gerente'),
]