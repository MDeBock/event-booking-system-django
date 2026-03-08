from django.contrib import admin
from .models import TipoEvento, Adicional, Salon, Paquete

@admin.register(TipoEvento)
class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Adicional)
class AdicionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_actual')
    search_fields = ('nombre',)
    list_filter = ('precio_actual',)

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad_maxima', 'precio_base')
    search_fields = ('nombre',)
    # Mejora la interfaz gráfica para seleccionar múltiples adicionales
    filter_horizontal = ('adicionales_disponibles',)

@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('nombre_combo', 'tipo_evento', 'salon', 'precio_paquete_actual', 'max_invitados')
    search_fields = ('nombre_combo',)
    list_filter = ('tipo_evento', 'salon')
    # Mejora la interfaz gráfica para los adicionales incluidos en el paquete
    filter_horizontal = ('adicionales_incluidos',)