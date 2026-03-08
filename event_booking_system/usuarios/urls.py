from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Usamos las vistas nativas de Django para mayor seguridad
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    
    # Vista personalizada para el panel de cliente
    path('panel/', views.panel_cliente, name='panel'),
]