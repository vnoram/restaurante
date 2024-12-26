from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .forms import PlatilloForm
from .models import Platillo, Compra, Pedido
from .forms import ReservaForm  # Importar el formulario
from django.contrib import messages
from core.forms import CustomUserCreationForm  # Usar el formulario personalizado
from .models import Reserva
from .forms import AddWaiterForm
from .forms import AddChefForm


from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    user = request.user

    # Identificar roles del usuario
    is_admin = user.is_authenticated and user.is_superuser
    is_chef = user.groups.filter(name='Chef').exists()
    is_waiter = user.groups.filter(name='Waiter').exists()
    is_client = user.groups.filter(name='cliente').exists()

    # Contexto para pasar a la plantilla
    context = {
        'is_admin': is_admin,
        'is_chef': is_chef,
        'is_waiter': is_waiter,
        'is_client': is_client,
    }

    return render(request, 'core/home.html', context)




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
    user = request.user  # Usuario autenticado

    # Determina el rol del usuario
    user_role = "Usuario no asignado"
    if user.groups.filter(name="cliente").exists():
        user_role = "Cliente"
    elif user.groups.filter(name="waiter").exists():
        user_role = "Camarero"

    # Redirige si no es cliente o camarero
    if user_role not in ["Cliente", "Camarero"]:
        return redirect("home")

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)  # No guarda aún en la base de datos
            reserva.cliente = user  # Asocia la reserva al usuario autenticado
            reserva.save()  # Guarda finalmente en la base de datos
            messages.success(request, "Reserva realizada con éxito.")
            return redirect("home")
    else:
        form = ReservaForm()

    return render(request, "core/reserve.html", {"form": form, "user_role": user_role})

#?------------------------------------------------------------------------------

# Vista para ver las reservas del usuario
@login_required
def reservations_list(request):
    user = request.user
    reservations = []
    is_waiter = False

    if user.groups.filter(name="cliente").exists():
        # Mostrar solo las reservas del cliente
        reservations = Reserva.objects.filter(cliente=user)
    elif user.groups.filter(name="waiter").exists():
        # Mostrar todas las reservas si es camarero
        reservations = Reserva.objects.all()
        is_waiter = True
    else:
        # Si no es cliente ni camarero, redirigir a home
        return redirect("home")

    return render(
        request, "core/reservations_list.html", {"reservations": reservations, "is_waiter": is_waiter}
    )
#?--------------------------------------------------------------------------------------------
#editar la reserva
@login_required
def edit_reservation_view(request, reservation_id):
    try:
        reservation = Reserva.objects.get(id=reservation_id)

        # Verifica que el usuario sea el cliente o camarero
        if not (
            request.user.groups.filter(name="cliente").exists() and reservation.cliente == request.user
        ) and not request.user.groups.filter(name="waiter").exists():
            return redirect("home")

        if request.method == "POST":
            form = ReservaForm(request.POST, instance=reservation)
            if form.is_valid():
                form.save()
                messages.success(request, "Reserva actualizada correctamente.")
                return redirect("reservations_list")
        else:
            form = ReservaForm(instance=reservation)
    except Reserva.DoesNotExist:
        messages.error(request, "La reserva no existe.")
        return redirect("reservations_list")

    return render(request, "core/edit_reservations.html", {"form": form, "reservations": reservation})

#?----------------------------------------------------------------------------------------------------
#eliminar reserva
@login_required
def delete_reservation_view(request, reservation_id):
    try:
        reservation = Reserva.objects.get(id=reservation_id)
    except Reserva.DoesNotExist:
        messages.error(request, "La reserva no existe.")
        return redirect("reservations_list")

    user = request.user
    is_waiter = user.groups.filter(name="waiter").exists()

    # Permitir eliminación solo si es cliente dueño de la reserva o un camarero
    if reservation.cliente != user and not is_waiter:
        messages.error(request, "No tienes permiso para eliminar esta reserva.")
        return redirect("reservations_list")

    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Reserva eliminada con éxito.")
        return redirect("reservations_list")

    return render(request, "core/confirm_delete.html", {"reservation": reservation})

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
# Función para registrar usuarios y asignarles un grupo por defecto como cliente
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

        # Asignar automáticamente al grupo "cliente"
        group_obj, created = Group.objects.get_or_create(name='cliente')
        user.groups.add(group_obj)  # Asignar el grupo "cliente" al usuario

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

    #return render(request, 'core/menu.html', {'form': form})
    return render(request, 'core/add_platillo.html', {'form': form})


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
@login_required
@user_passes_test(is_admin)  # Solo admins pueden acceder
def add_waiter_view(request):
    if request.method == 'POST':
        form = AddWaiterForm(request.POST)
        if form.is_valid():
            waiter = form.save(commit=False)
            waiter.set_password(form.cleaned_data['password'])  # Asegúrate de hashear el password
            waiter.save()
            
            # Asignar al grupo 'waiter' (o camarero)
            waiter_group, created = Group.objects.get_or_create(name='waiter')
            waiter.groups.add(waiter_group)
            
            messages.success(request, 'Camarero agregado exitosamente.')
            form = AddWaiterForm()
            return redirect('manage_user')  # Redirige a la gestión de usuarios
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        # Inicializa un formulario vacío para solicitudes GET
        form = AddWaiterForm()
    return render(request, 'core/add_waiter.html', {'form': form})

#!----------------------------------------------------------------------------

# compras para clientes

@login_required
def comprar_view(request):
    if not request.user.groups.filter(name='Cliente').exists():
        messages.error(request, "Solo los clientes pueden realizar compras.")
        return redirect('menu')

    # Obtener los platillos disponibles
    platillos = Platillo.objects.filter(disponible=True)

    if request.method == 'POST':
        platillos_ids = request.POST.getlist('platillos')
        if not platillos_ids:
            messages.error(request, "No seleccionaste ningún platillo.")
        else:
            # Crear la compra
            compra = Compra.objects.create(cliente=request.user)

            # Registrar los pedidos
            for platillo_id in platillos_ids:
                platillo = get_object_or_404(Platillo, id=platillo_id, disponible=True)
                Pedido.objects.create(compra=compra, platillo=platillo)

            # Agregar mensaje de éxito
            messages.success(request, "¡Compra realizada con éxito!")
        
        # Renderizar la página nuevamente sin redirigir
        return render(request, 'core/comprar.html', {'platillos': platillos})

    return render(request, 'core/comprar.html', {'platillos': platillos})

#? ver compras y calcular el total de 
@login_required
def ver_compras_view(request):
    """Muestra al cliente las compras realizadas por él, incluyendo el total."""
    if not request.user.groups.filter(name='Cliente').exists():
        return redirect('menu')

    # Obtener todas las compras del cliente
    compras = Compra.objects.filter(cliente=request.user).prefetch_related('pedidos__platillo')

    # Agregar el total de cada compra al contexto
    for compra in compras:
        compra.total = sum(pedido.platillo.precio for pedido in compra.pedidos.all())

    return render(request, 'core/ver_compras.html', {'compras': compras})

#?-------------------------------------------------------------------------
# Agregar chefs
@login_required
@user_passes_test(is_admin)  # Solo admins pueden acceder
def add_chef_view(request):
    if request.method == 'POST':
        form = AddChefForm(request.POST)  # Usa el formulario para añadir chefs
        if form.is_valid():
            chef = form.save(commit=False)

            chef.set_password(form.cleaned_data['password'])  # Asegúrate de hashear el password
            chef.save()
            
            # Asignar al grupo 'chef'
            chef_group, created = Group.objects.get_or_create(name='chef')
            chef.groups.add(chef_group)
            
            messages.success(request, 'Chef agregado exitosamente.')
            form = AddChefForm()
            return redirect('manage_user')  # Redirige a la gestión de usuarios
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        # Inicializa un formulario vacío para solicitudes GET
        form = AddChefForm()
    return render(request, 'core/add_chef.html', {'form': form})

#?-------------------------------------------------------------------------
#funcion para que los chefs visualicen las compras echas por los clientes


@login_required
def ver_compras_chef(request):
    if not request.user.groups.filter(name='Chef').exists():
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

    compras = Compra.objects.all()
    return render(request, 'core/ver_compras_chef.html', {'compras': compras})


#?--------------------------------------------
#funcion para que los chefs cambien el estado de las compras
@login_required
def actualizar_estado_compra(request, compra_id):
    if not request.user.groups.filter(name='Chef').exists():
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

    compra = get_object_or_404(Compra, id=compra_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['en_preparacion', 'terminado', 'compra_cancelada']:
            compra.estado = nuevo_estado
            compra.save()
            messages.success(request, "Estado de la compra actualizado con éxito.")
        else:
            messages.error(request, "Estado inválido.")

    return redirect('ver_compras_chef')


