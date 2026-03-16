from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Trae automáticamente tu modelo 'CustomUser'
User = get_user_model() 

class RegistroClienteForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Si quisieras pedirle el email al registrarse, se agrega acá:
        # fields = UserCreationForm.Meta.fields + ('email',)