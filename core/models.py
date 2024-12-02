from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError





# Modelo para los ítems del menú
class MenuItem(models.Model):
    """
    Representa un ítem en el menú del restaurante.
    """
    name = models.CharField(max_length=100)  # Nombre del ítem
    description = models.TextField()  # Descripción del ítem
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del ítem

    def __str__(self):
        return self.name  # Devuelve el nombre del ítem como representación



# Modelo para los camareros
class Waiter(models.Model):
    """
    Representa a un camarero del restaurante.
    """
    full_name = models.CharField(max_length=100)  # Nombre completo del camarero
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del perfil

    def __str__(self):
        return self.full_name  # Representación del camarero

#modelos para los platillos
class Platillo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Asegúrate de valores positivos
    imagen = models.ImageField(upload_to='platillos/', blank=True, null=True)

    def clean(self):
        if self.precio < 0:
            raise ValidationError({'precio': 'El precio no puede ser negativo.'})

    def __str__(self):
        return self.nombre
    

#user = models.ForeignKey(User, on_delete=models.CASCADE)

# Modelo para las reservas
class Reserva(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, null=True, blank=True)
    #cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con Cliente
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, null=True)  # Menú relacionado
    reservation_date = models.DateTimeField()  # Fecha y hora de la reserva
    numero_personas = models.PositiveIntegerField()  # Número de invitados
    comentarios = models.TextField(blank=True, null=True)  # Comentarios opcionales

    def __str__(self):
        return f"Reserva de {self.cliente.user.username} para {self.numero_personas} personas el {self.reservation_date}"

#? identificador unico para los clientes
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación 1 a 1 con User
    identificador_unico = models.CharField(max_length=20, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Información opcional
    direccion = models.TextField(blank=True, null=True)  # Información opcional

    def save(self, *args, **kwargs):
        # Generar identificador único solo si no existe
        if not self.identificador_unico:
            self.identificador_unico = f"CL-{self.user.id:06}"  # Ejemplo: CL-000123
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.identificador_unico}"