from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    # Catálogo público
    path('', views.lista_salones, name='lista_salones'),
    path('promociones/', views.promociones, name='promociones'), # NUEVA RUTA
    
    # Gestión interna (Staff)
    path('gestion/nuevo/', views.crear_salon, name='crear_salon'),
]