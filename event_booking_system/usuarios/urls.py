from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('panel/', views.panel_cliente, name='panel'),
    # NUEVA RUTA:
    path('registro/', views.registro, name='registro'),
]