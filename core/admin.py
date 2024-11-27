from django.contrib import admin
from .models import MenuItem, Reserva, Waiter

# Configuración para el modelo MenuItem
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Configuración para administrar los ítems del menú.
    """
    list_display = ('name', 'price', 'description')  # Campos a mostrar en la lista de admin
    search_fields = ('name',)  # Permite buscar por nombre

# Configuración para el modelo Reserva
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """
    Configuración para administrar las reservas.
    """
    list_display = ('reservation_date', 'numero_personas', 'comentarios')  # Campos a mostrar en la lista de admin
    search_fields = ('reservation_date',)  # Permite buscar por fecha
    list_filter = ('reservation_date',)  # Filtro por fecha de reserva

# Configuración para el modelo Waiter
@admin.register(Waiter)
class WaiterAdmin(admin.ModelAdmin):
    """
    Configuración para administrar los camareros.
    """
    list_display = ('full_name', 'created_at')  # Campos a mostrar en la lista de admin
    search_fields = ('full_name',)  # Permite buscar por nombre completo
    list_filter = ('created_at',)  # Filtro por fecha de creación
