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
    nombre = models.CharField(max_length=100)  # Campo para el nombre del platillo.
    descripcion = models.TextField()  # Descripción del platillo.
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Campo para el precio, con validación de valores positivos.
    imagen = models.ImageField(upload_to='platillos/', blank=True, null=True)  # Campo opcional para subir una imagen.
    disponible = models.BooleanField(default=True)  # Campo para disponibilidad

    def clean(self):
        """
        Valida que el precio sea mayor a 0 antes de guardar el modelo.
        """
        if self.precio is None or self.precio <= 0:
            raise ValidationError("El precio debe ser mayor a 0.")
        super().clean()  # Llama al método clean de la clase padre.

    def __str__(self):
        """
        Representación legible del modelo.
        """
        return self.nombre
    

#user = models.ForeignKey(User, on_delete=models.CASCADE)

# Modelo para las reservas

class Reserva(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True)
    reservation_date = models.DateTimeField()
    numero_personas = models.PositiveIntegerField()
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.cliente.username} para {self.numero_personas} personas el {self.reservation_date}"
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
    
#? modelos de compra cliente


class Compra(models.Model):
    ESTADOS_COMPRA = [
        ('en_preparacion', 'En Preparación'),
        ('terminado', 'Terminado'),
        ('compra_cancelada', 'Compra Cancelada'),
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_COMPRA,
        default='en_preparacion'
    )
    def __str__(self):
        return f"Compra {self.id} - {self.get_estado_display()}"

class Pedido(models.Model):
    compra = models.ForeignKey(Compra, related_name="pedidos", on_delete=models.CASCADE)
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.platillo.nombre} (Compra #{self.compra.id})"