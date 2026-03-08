from django.views.generic import ListView
from .models import Salon

class SalonListView(ListView):
    model = Salon
    # Le indicamos exactamente en qué subcarpeta buscar el HTML (tu buena práctica)
    template_name = 'catalogo/lista_salones.html' 
    # Cómo se va a llamar la variable que recibe el HTML con los datos
    context_object_name = 'salones' 

    def get_queryset(self):
        # Traemos todos los salones ordenados alfabéticamente
        return Salon.objects.all().order_by('nombre')