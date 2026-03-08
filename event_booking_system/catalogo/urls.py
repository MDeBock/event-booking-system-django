from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    # La ruta vacía '' significa que responderá a /catalogo/
    path('', views.SalonListView.as_view(), name='lista_salones'),
]