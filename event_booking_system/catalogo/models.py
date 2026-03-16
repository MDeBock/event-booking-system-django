from django.db import models
from django.core.files import File
from io import BytesIO
from PIL import Image
import os

class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Evento")

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
    
    # Imagen de portada del salón
    imagen_portada = models.ImageField(upload_to='salones/portadas/', null=True, blank=True, verbose_name="Imagen de Portada")
    
    adicionales_disponibles = models.ManyToManyField(Adicional, blank=True, related_name='salones')

    class Meta:
        verbose_name = "Salón"
        verbose_name_plural = "Salones"

    def save(self, *args, **kwargs):
        # Lógica de conversión automática a WebP para la portada
        if self.imagen_portada:
            if not self.imagen_portada.name.lower().endswith('.webp'):
                img = Image.open(self.imagen_portada)
                if img.mode in ("RGBA", "P"): 
                    img = img.convert("RGB")
                
                # Achica la imagen si es gigantesca, manteniendo la proporción
                img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='WEBP', quality=80) # Calidad al 80% (óptimo para web)
                output.seek(0)
                
                # Le cambiamos la extensión al nombre original
                nombre_base = os.path.splitext(self.imagen_portada.name)[0]
                self.imagen_portada = File(output, name=f"{nombre_base}.webp")
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} (Capacidad: {self.capacidad_maxima})"


# EL MODELO QUE ME HABÍA COMIDO:
class Paquete(models.Model):
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name='paquetes')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='paquetes')
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


class GaleriaImagen(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='galeria')
    imagen = models.ImageField(upload_to='salones/galeria/')
    descripcion = models.CharField(max_length=100, blank=True, null=True, help_text="Ej: Vista de la pista de baile")

    class Meta:
        verbose_name = "Imagen de Galería"
        verbose_name_plural = "Imágenes de Galería"

    def save(self, *args, **kwargs):
        # Lógica de conversión automática a WebP para la galería
        if self.imagen:
            if not self.imagen.name.lower().endswith('.webp'):
                img = Image.open(self.imagen)
                if img.mode in ("RGBA", "P"): 
                    img = img.convert("RGB")
                
                img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='WEBP', quality=80)
                output.seek(0)
                
                nombre_base = os.path.splitext(self.imagen.name)[0]
                self.imagen = File(output, name=f"{nombre_base}.webp")
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Imagen para {self.salon.nombre}"