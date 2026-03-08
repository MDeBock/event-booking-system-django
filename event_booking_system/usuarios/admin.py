from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Agregamos los campos extra a la pantalla de edición del usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('telefono', 'dni')}),
    )
    # Agregamos los campos extra a la pantalla de creación de usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('telefono', 'dni')}),
    )
    
    # Columnas que se ven en el listado principal
    list_display = ('username', 'email', 'first_name', 'last_name', 'telefono', 'dni', 'is_staff')
    
    # Campos por los que el buscador puede filtrar
    search_fields = ('username', 'email', 'first_name', 'last_name', 'dni')