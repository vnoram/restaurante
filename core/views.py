from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .forms import PlatilloForm
from .models import Platillo
from .forms import ReservaForm  # Importar el formulario
from django.contrib import messages
from core.forms import CustomUserCreationForm  # Usar el formulario personalizado
from .models import Reserva
from .forms import AddWaiterForm



# Vista para la página de inicio
def home_view(request):
    user = request.user
    is_admin = False
    if user.is_authenticated:
        # Verifica si el usuario es administrador
        is_admin = user.groups.filter(name='admin').exists()
    return render(request, 'core/home.html', {'is_admin': is_admin})


# Vista del menú
def menu_view(request):
    # Obtener todos los platillos de la base de datos
    platillos = Platillo.objects.all()  # Esto obtiene todos los platillos

    # Pasamos los platillos al template 'core/menu.html'
    return render(request, 'core/menu.html', {'platillos': platillos, 'user_role': user_role})

#?-------------------------------------

@login_required
def menu_view(request):
    
    # Obtener el rol del usuario
    if request.user.groups.filter(name='cliente').exists():
        user_role = 'Cliente'
    elif request.user.groups.filter(name='waiter').exists():
        user_role = 'Camarero'
    elif request.user.groups.filter(name='admin').exists():
        user_role = 'Administrador'
    else:
        user_role = 'Usuario no asignado'

    # Pasar el rol al contexto
    return render(request, 'core/menu.html', {'user_role': user_role})

#?----------------------------------------------

# Vista para ver las reservas del usuario
@login_required
def reservations_list(request):
    reservations = Reserva.objects.all()  # Obtén todas las reservaciones
    return render(request, 'core/reservations_list.html', {'reservations': reservations})


#!-----------------------------------------------------
# Vista para reservar
@login_required
def reserve_view(request):
    # Solo los clientes y meseros pueden hacer reservas
    user_role = 'Usuario no asignado'
    if request.user.groups.filter(name='cliente').exists():
        user_role = 'Cliente'
    elif request.user.groups.filter(name='waiter').exists():
        user_role = 'Camarero'

    # Si no es un cliente o mesero, redirigir a home
    if user_role not in ['Cliente', 'Camarero']:
        return redirect('home')

    # Manejo del formulario
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la reserva
            messages.success(request, 'Reserva realizada con éxito.')
            return redirect('home')  # Redirige al home después de guardar
    else:
        form = ReservaForm()  # Si es GET, se crea un formulario vacío

    # Renderiza el formulario con el rol del usuario
    return render(request, 'core/reserve.html', {'form': form, 'user_role': user_role})
#!--------------------------------------------------------
# Vista para el dashboard del camarero
@login_required
def waiter_dashboard_view(request):
    if not request.user.groups.filter(name='waiter').exists():
        return redirect('home')
    return render(request, 'core/waiter_dashboard.html')

# Vista para el dashboard del administrador
@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        return redirect('home')
    return render(request, 'core/admin_dashboard.html')

# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'registration/login.html')

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('home')

#!-----------------------------------------------------------
# Función para registrar usuarios y asignarles un grupo
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')  # Asegúrate de obtener el email

        # Verificar si el nombre de usuario existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('register')

        # Verificar si el correo electrónico ya existe
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está en uso.')
            return redirect('register')

        # Crear el nuevo usuario
        user = User.objects.create_user(username=username, password=password, email=email)

        group = request.POST.get('group')  # Puede ser 'admin', 'waiter', 'cliente'
        if group:
            group_obj, created = Group.objects.get_or_create(name=group)
            user.groups.add(group_obj)  # Asignar el grupo al usuario

        user.save()
        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('login')  # Redirige al login

    return render(request, 'registration/register.html')

#!-----------------------------------------------------------------------------
#? funciones para verificar usuarios
# Función para verificar si el usuario es un 'cliente'
def is_client(user):
    return user.groups.filter(name='cliente').exists()

# Función para verificar si el usuario es un 'waiter'
def is_waiter(user):
    return user.groups.filter(name='waiter').exists()

# Función para verificar si el usuario es un 'admin'
def is_admin(user):
    return user.groups.filter(name='admin').exists()

# Vista para la página de inicio de acuerdo al grupo
@login_required
@user_passes_test(is_client)  # Verifica si el usuario es un cliente
def cliente_dashboard(request):
    return render(request, 'core/cliente_dashboard.html')

@login_required
@user_passes_test(is_waiter)  # Verifica si el usuario es un camarero
@login_required
def waiter_dashboard(request):
    # Obtener las reservas o los datos necesarios
    reservations = Reservation.objects.all()  # Ejemplo de cómo obtener las reservas

    return render(request, 'core/waiter_dashboard.html', {'reservations': reservations})


@login_required
@user_passes_test(is_admin)  # Verifica si el usuario es un administrador
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')

# Vista para login, si no está logueado redirige

@login_required
def home_view(request):
    user = request.user
    is_admin = False
    
    # Verifica si el usuario es parte del grupo admin
    if user.is_authenticated:
        is_admin = user.groups.filter(name='admin').exists()

    # Pasa la variable is_admin a la plantilla
    return render(request, 'core/home.html', {'is_admin': is_admin})
# Página predeterminada si no pertenece a ningún grupo



#!-------------------------------------

#? platillos

# Vista para mostrar el menú y agregar platillos
@login_required
def menu_view(request):
    platillos = Platillo.objects.all()  # Obtener todos los platillos de la base de datos
    user_role = 'Usuario no asignado'

    # Obtener el rol del usuario
    if request.user.groups.filter(name='cliente').exists():
        user_role = 'Cliente'
    elif request.user.groups.filter(name='waiter').exists():
        user_role = 'Camarero'
    elif request.user.groups.filter(name='admin').exists():
        user_role = 'Administrador'
    
    # Lógica para procesar el formulario si el usuario es administrador
    if request.method == 'POST' and user_role == 'Administrador':
        form = PlatilloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Guarda el nuevo platillo en la base de datos
            return redirect('menu')  # Redirige al menu después de agregar el platillo
    else:
        form = PlatilloForm()

    # Pasamos los platillos y el formulario al contexto
    return render(request, 'core/menu.html', {
        'platillos': platillos,
        'form': form,
        'user_role': user_role
    })

# Vista para agregar un platillo
@login_required
def add_platillo_view(request):
    if request.method == 'POST':
        form = PlatilloForm(request.POST, request.FILES)  # Asegúrate de permitir archivos si usas imagenes
        if form.is_valid():
            form.save()  # Guarda el platillo en la base de datos
            messages.success(request, 'Platillo agregado correctamente.')
            return redirect('menu')  # Redirige al menú una vez agregado el platillo
    else:
        form = PlatilloForm()
        messages.error(request, 'Corrige los errores del formulario.')

    return render(request, 'core/menu.html', {'form': form})

# Vista para eliminar un platillo
@login_required
def delete_platillo(request, platillo_id):
    # Verificar si el usuario es administrador
    if not request.user.groups.filter(name='admin').exists():
        return redirect('home')  # O redirigir a una página de acceso denegado si lo prefieres

    # Obtener el platillo que se desea eliminar
    platillo = get_object_or_404(Platillo, id=platillo_id)

    if request.method == 'POST':
        platillo.delete()  # Eliminar el platillo
        return redirect('menu')  # Redirigir al menú después de eliminar

    # Si no es POST, solo mostrar la página de confirmación
    return render(request, 'core/confirm_delete.html', {'platillo': platillo})



#!--------------------------------------------------------------------------------------------------------------
# Decorador para asegurar que solo los admins accedan
def is_admin(user):
    return user.is_staff  # Solo los usuarios con el atributo `is_staff` serán considerados administradores.

@user_passes_test(is_admin)

def manage_user_view(request):
    users = User.objects.all()
    users_with_roles = []
    for user in users:
        group = user.groups.first()  # Obtiene el primer grupo al que pertenece el usuario
        role = group.name if group else "Sin rol"  # Si no tiene grupo, muestra "Sin rol"
        users_with_roles.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role
        })
    return render(request, 'core/manage_user.html', {'users': users_with_roles})

@user_passes_test(is_admin)
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:  # Evitar eliminar al superusuario
        messages.error(request, "No puedes eliminar al superusuario.")
        return redirect('manage_user')
    user.delete()
    messages.success(request, f"El usuario {user.username} ha sido eliminado.")
    return redirect('manage_user')

#agregar usuarios
@user_passes_test(is_admin)
def add_user_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('manage_user')
    else:
        form = UserCreationForm()
    return render(request, 'core/add_user.html', {'form': form})

#agregar camareros
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def add_waiter_view(request):
    if request.method == 'POST':
        form = AddWaiterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_user')  # Redirige a la gestión de usuarios
    else:
        form = AddWaiterForm()
    return render(request, 'core/add_waiter.html', {'form': form})
