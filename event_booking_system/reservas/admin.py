from django.contrib import admin
from .models import Reserva, ReservaAdicional, Resena

class ReservaAdicionalInline(admin.TabularInline):
    model = ReservaAdicional
    extra = 1
    # Bloqueamos el precio histórico para que nadie lo pueda editar a mano
    readonly_fields = ('precio_historico_adicional',)
    
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'salon', 'fecha_hora_inicio', 'estado', 'monto_abonado', 'ver_saldo_a_pagar')
    list_filter = ('estado', 'salon', 'tipo_evento')
    search_fields = ('cliente__username', 'cliente__dni', 'id')
    
    # Bloqueamos el precio histórico del salón y agregamos las propiedades calculadas
    readonly_fields = ('precio_historico_salon', 'fecha_creacion', 'ver_total_historico', 'ver_total_actual', 'ver_saldo_a_pagar')
    
    inlines = [ReservaAdicionalInline]

    def ver_total_historico(self, obj):
        return f"${obj.total_historico}"
    ver_total_historico.short_description = "Total Histórico"

    def ver_total_actual(self, obj):
        return f"${obj.total_actual}"
    ver_total_actual.short_description = "Total Actual (Hoy)"

    def ver_saldo_a_pagar(self, obj):
        return f"${obj.saldo_a_pagar}"
    ver_saldo_a_pagar.short_description = "Saldo Pendiente"

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'calificacion', 'fecha_publicacion')
    list_filter = ('calificacion',)
    search_fields = ('reserva__cliente__username', 'comentario')