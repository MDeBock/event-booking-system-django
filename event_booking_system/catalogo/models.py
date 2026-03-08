from django.db import models

class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Evento (Ej: 15 Años, Corporativo)")

    class Meta:
        verbose_name = "Tipo de Evento"
        verbose_name_plural = "Tipos de Eventos"

    def __str__(self):
        return self.nombre


class Adicional(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio actual del servicio")

    class Meta:
        verbose_name = "Servicio Adicional"
        verbose_name_plural = "Servicios Adicionales"

    def __str__(self):
        return f"{self.nombre} - ${self.precio_actual}"


class Salon(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    capacidad_maxima = models.PositiveIntegerField(help_text="Cantidad máxima de personas permitidas")
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio actual del alquiler")
    
    # Relación muchos a muchos: Qué adicionales se pueden ofrecer en este salón
    adicionales_disponibles = models.ManyToManyField(Adicional, blank=True, related_name='salones')

    class Meta:
        verbose_name = "Salón"
        verbose_name_plural = "Salones"

    def __str__(self):
        return f"{self.nombre} (Capacidad: {self.capacidad_maxima})"


class Paquete(models.Model):
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name='paquetes')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='paquetes')
    # Un paquete incluye varios adicionales
    adicionales_incluidos = models.ManyToManyField(Adicional, blank=True, related_name='paquetes')
    
    nombre_combo = models.CharField(max_length=150, help_text="Ej: Fiesta 15 Oro")
    descripcion = models.TextField(blank=True, null=True)
    max_invitados = models.PositiveIntegerField()
    precio_paquete_actual = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio total cerrado por el combo")

    class Meta:
        verbose_name = "Paquete / Combo"
        verbose_name_plural = "Paquetes / Combos"

    def __str__(self):
        return f"{self.nombre_combo} - {self.tipo_evento.nombre}"