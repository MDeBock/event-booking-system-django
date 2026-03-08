from django.db import models
from django.conf import settings
from catalogo.models import Salon, TipoEvento, Paquete, Adicional
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from decimal import Decimal

class Reserva(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),     
        ('Confirmada', 'Confirmada'),   
        ('Finalizada', 'Finalizada'),   
        ('Cancelada', 'Cancelada'),     
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT, related_name='reservas')
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    paquete = models.ForeignKey(Paquete, on_delete=models.SET_NULL, null=True, blank=True, help_text="Dejar en blanco si es a medida")
    
    fecha_hora_inicio = models.DateTimeField(help_text="Cuándo ingresa el cliente/organización")
    fecha_hora_liberacion = models.DateTimeField(help_text="Cuándo termina la limpieza y se libera el salón")
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    
    # Precios históricos con blank=True y null=True para que se autocompleten solos
    precio_historico_salon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Se autocompleta con el precio del salón/paquete al reservar")
    monto_abonado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Dinero ingresado (seña o total)")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        unique_together = ('salon', 'fecha_hora_inicio')

    def save(self, *args, **kwargs):
        # Autocompletado del precio histórico
        if not self.precio_historico_salon:
            if self.paquete:
                self.precio_historico_salon = self.paquete.precio_paquete_actual
            elif self.salon:
                self.precio_historico_salon = self.salon.precio_base
            else:
                self.precio_historico_salon = Decimal('0.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente.username} - {self.fecha_hora_inicio.strftime('%d/%m/%Y')}"

    @property
    def total_historico(self):
        if not self.pk:
            return Decimal('0.00')
            
        precio_salon = self.precio_historico_salon or Decimal('0.00')
        total_extras = sum((extra.precio_historico_adicional or Decimal('0.00')) for extra in self.extras_contratados.all())
        return precio_salon + total_extras

    @property
    def total_actual(self):
        if not self.pk:
            return Decimal('0.00')
            
        if self.paquete:
            precio_base_hoy = self.paquete.precio_paquete_actual
        elif self.salon:
            precio_base_hoy = self.salon.precio_base
        else:
            precio_base_hoy = Decimal('0.00')
            
        total_extras_hoy = sum(extra.adicional.precio_actual for extra in self.extras_contratados.all())
        return precio_base_hoy + total_extras_hoy

    @property
    def saldo_a_pagar(self):
        if not self.pk or not self.fecha_creacion:
            return Decimal('0.00')
            
        fecha_limite_congelamiento = self.fecha_creacion + timedelta(days=7)
        monto_pagado = self.monto_abonado or Decimal('0.00')
        
        if timezone.now() > fecha_limite_congelamiento:
            saldo = self.total_actual - monto_pagado
        else:
            saldo = self.total_historico - monto_pagado
            
        return max(saldo, Decimal('0.00'))


class ReservaAdicional(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='extras_contratados')
    adicional = models.ForeignKey(Adicional, on_delete=models.PROTECT)
    precio_historico_adicional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Se autocompleta con el precio actual del extra")

    class Meta:
        verbose_name = "Adicional de Reserva"
        verbose_name_plural = "Adicionales de Reserva"

    def clean(self):
        super().clean()
        # EL ESCUDO: Verificamos si el adicional está en la lista de permitidos del salón
        if hasattr(self, 'reserva') and hasattr(self, 'adicional'):
            if self.reserva.salon and self.adicional:
                if self.adicional not in self.reserva.salon.adicionales_disponibles.all():
                    raise ValidationError({
                        'adicional': f'Error: El servicio "{self.adicional.nombre}" no está disponible para el salón "{self.reserva.salon.nombre}".'
                    })

    def save(self, *args, **kwargs):
        # Autocompletado del precio del adicional
        if not self.precio_historico_adicional and self.adicional:
            self.precio_historico_adicional = self.adicional.precio_actual
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.adicional.nombre} en Reserva #{self.reserva.id}"


class Resena(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='resena')
    calificacion = models.PositiveSmallIntegerField(help_text="Puntuación del 1 al 5")
    comentario = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f"Reseña de Reserva #{self.reserva.id} - {self.calificacion} Estrellas"