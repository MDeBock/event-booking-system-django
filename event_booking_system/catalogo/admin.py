from django.contrib import admin
from .models import TipoEvento, Adicional, Salon, GaleriaImagen, Paquete

@admin.register(TipoEvento)
class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Adicional)
class AdicionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_actual')
    search_fields = ('nombre',)
    list_filter = ('precio_actual',)

# Permite cargar fotos de la galería directamente al crear/editar el salón
class GaleriaImagenInline(admin.TabularInline):
    model = GaleriaImagen
    extra = 3  
    fields = ('imagen', 'descripcion')

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad_maxima', 'precio_base')
    search_fields = ('nombre',)
    filter_horizontal = ('adicionales_disponibles',)
    inlines = [GaleriaImagenInline]

# EL ADMIN DEL PAQUETE QUE ME HABÍA COMIDO:
@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('nombre_combo', 'tipo_evento', 'salon', 'precio_paquete_actual', 'max_invitados')
    search_fields = ('nombre_combo',)
    list_filter = ('tipo_evento', 'salon')
    filter_horizontal = ('adicionales_incluidos',)