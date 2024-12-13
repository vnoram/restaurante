from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Platillo
from .models import Reserva
from django.core.exceptions import ValidationError
from django.utils.timezone import now



# Formulario personalizado para registrar usuarios
class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para registrar nuevos usuarios.
    Hereda de UserCreationForm para extender sus funcionalidades.
    """
    email = forms.EmailField(required=True, help_text="Introduce una dirección de correo válida.")  # Campo adicional para el correo electrónico

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Campos del formulario

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

        

#formulario para platillos
class PlatilloForm(forms.ModelForm):
    class Meta:
        model = Platillo
        fields = ['nombre', 'descripcion', 'precio', 'imagen']

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

# Formulario para las reservas
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['reservation_date', 'numero_personas', 'comentarios']
        widgets = {
            'reservation_date': forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comentarios': forms.Textarea(attrs={'placeholder': 'Comentarios (opcional)'}),
        }

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data.get('reservation_date')
        if reservation_date < now():
            raise ValidationError("No puedes realizar una reserva para una fecha pasada.")
        return reservation_date

#formulario para agregar camareros
class AddWaiterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(AddWaiterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.initial = None  # Esto asegura que no haya datos iniciales en el formulario


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            waiter_group = Group.objects.get(name='camarero')
            user.groups.add(waiter_group)
        return user

#comprar

class PlatilloForm(forms.ModelForm):
    class Meta:
        model = Platillo
        fields = ['nombre', 'descripcion', 'precio', 'imagen']

#creacion de chef
# Formulario para agregar chefs
class AddChefForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(AddChefForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.initial = None  # Esto asegura que no haya datos iniciales en el formulario

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Asegura que la contraseña esté hasheada
        if commit:
            user.save()
            # Asignar al grupo "Chef"
            chef_group, _ = Group.objects.get_or_create(name='chef')
            user.groups.add(chef_group)
        return user
