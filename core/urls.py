from django.urls import path
from . import views  # Importamos las vistas desde el archivo views.py de la app `core`

urlpatterns = [
    path('', views.home_view, name='home'),  # Página de inicio
    path('menu/', views.menu_view, name='menu'),  # Vista del menú
    path('reserve/', views.reserve_view, name='reserve'),  # URL para hacer una reserva
    path('reservations_list/', views.reservations_list, name='reservations_list'),  # URL para ver las reservas
    path('waiter_dashboard/', views.waiter_dashboard_view, name='waiter_dashboard'),  # Dashboard para camareros
    path('cliente_dashboard/', views.cliente_dashboard, name='cliente_dashboard'),  # Vista cliente
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),  # Dashboard para administradores
    path('login/', views.login_view, name='login'),  # Vista para iniciar sesión
    path('logout/', views.logout_view, name='logout'),  # Vista para cerrar sesión
    path('register/', views.register_view, name='register'),  # Vista para registrar usuarios
    path('add_platillo/', views.add_platillo_view, name='add_platillo'),  # Nueva URL para agregar platillos
    path('delete_platillo/<int:platillo_id>/', views.delete_platillo, name='delete_platillo'),  # Ruta para eliminar platillo


]
