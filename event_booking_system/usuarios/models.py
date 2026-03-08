from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Django ya incluye por defecto: username, password, email, first_name, last_name, is_staff, is_superuser, etc.
    
    telefono = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name='Teléfono'
    )
    dni = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        unique=True, 
        verbose_name='DNI'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        # Si tiene nombre cargado lo muestra, si no, cae en el username
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name} ({self.username})"
        return self.username