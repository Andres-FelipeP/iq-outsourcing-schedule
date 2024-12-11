from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, UserEditForm, ReservaForm
from .models import User, TipoUsuario, Reserva
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from django.urls import reverse
from django.utils.safestring import mark_safe


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Redireccionar basado en el tipo de usuario
            if user.tipo_usuario == 'coordinador':
                return redirect('home_empleado')
            elif user.tipo_usuario == 'empleado':
                return redirect('home_empleado')
            elif user.tipo_usuario == 'admin':
                return redirect('home_admin')
    else:
        form = AuthenticationForm()

    return render(request, 'landing.html', {'form': form})


@login_required
def registrar(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES, prefix='user')
        if user_form.is_valid():
            user_form.save()

        return redirect('home_admin')
    else:
        user_form = CustomUserCreationForm(prefix='user')

    return render(request, 'registrar_personal.html', {'user_form': user_form})


@login_required

def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required

def home_admin(request):
    reservas = Reserva.objects.all()
    eventos = [
        {

            "title": f"{reserva.usuario.nombre[0]}. {reserva.usuario.apellido1} {reserva.usuario.apellido2[0]}. ({reserva.turno})",
            "start": str(reserva.fecha),
            "color": "red" if reserva.usuario.tipo_usuario == 'coordinador' else "blue",
            "description": f"Empleado: {reserva.usuario.cedula}, Turno: {reserva.turno}"

        }
        for reserva in reservas
    ]
    return render(request, 'home_admin.html', {'eventos': eventos, 'nombre': request.user.nombre, 'apellido1': request.user.apellido1, 'apellido2': request.user.apellido2,
        'cedula': request.user.cedula})


@login_required

def home_empleado(request):
    return render(request, 'home_empleado.html', {'nombre': request.user.nombre, 'apellido1': request.user.apellido1, 'apellido2': request.user.apellido2,
        'cedula': request.user.cedula})


@login_required

def usuarios_list(request):
    # Filtrar usuarios que sean coordinadores o empleados
    usuarios = User.objects.filter(tipo_usuario__in=[TipoUsuario.coordinador, TipoUsuario.empleado])
    context = {
        'usuarios': usuarios
    }
    return render(request, 'empleados_empresa.html', context)


@login_required

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    usuario.delete()
    messages.success(request, f"Usuario {usuario.nombre} eliminado con éxito.")
    return redirect('empleados')  # Redirige a la lista de usuarios

@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuario {usuario.nombre} actualizado con éxito.")
            return redirect('empleados')  # Redirige a la lista de usuarios
    else:
        form = UserEditForm(instance=usuario)
    return render(request, 'editar_empleado.html', {'form': form, 'usuario': usuario})



@login_required
def calendario(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        turno = request.POST.get('turno')

        if request.user.tipo_usuario == 'admin':
            messages.warning(request, "No tienes permisos para crear una reserva.")
            return redirect('calendario')

        if not fecha or not turno:
            messages.warning(request, "Selecciona una fecha y un turno.")
            return redirect('calendario_reservas')

        fecha = date.fromisoformat(fecha)
        usuario = request.user

        # Verificar si ya existe una reserva para este usuario en la misma fecha
        if Reserva.objects.filter(usuario=usuario, fecha=fecha).exists():
            messages.error(request, "Ya tienes una reserva para este día. Por favor, selecciona otra fecha.")
            return redirect('calendario_reservas')

        # Validación de coordinadores
        if usuario.tipo_usuario == 'coordinador':
            if fecha.weekday() != 4:  # No es viernes
                messages.error(request, "Los coordinadores solo pueden tomar descansos los viernes.")
                return redirect('calendario_reservas')

            if Reserva.objects.filter(fecha=fecha, turno=turno, usuario__tipo_usuario='coordinador').exists():
                messages.error(request, "Ya hay un coordinador en ese turno.")
                return redirect('calendario_reservas')

        # Validación de descanso cada 2 meses
        reserva = Reserva(usuario=usuario, fecha=fecha, turno=turno)
        if not reserva.es_valida():
            messages.error(request, "Solo puedes tomar un descanso cada 2 meses.")
            return redirect('calendario_reservas')

        reserva.save()
        messages.success(request, "Reserva creada exitosamente.")
        return redirect('calendario_reservas')
    reservas = Reserva.objects.all()
    eventos = [
        {

            "title": f"{reserva.usuario.nombre[0]}. {reserva.usuario.apellido1} {reserva.usuario.apellido2[0]}. ({reserva.turno})",
            "start": str(reserva.fecha),
            "color": "red" if reserva.usuario.tipo_usuario == 'coordinador' else "blue",
            "description": f"Empleado: {reserva.usuario.cedula}, Turno: {reserva.turno}"

    }
        for reserva in reservas
    ]
    return render(request, 'calendario.html', {'eventos': eventos})


def mis_reservas(request):
    # Asumiendo que el usuario está autenticado
    reservas = Reserva.objects.filter(usuario=request.user)

    return render(request, 'mis_reservas.html', {'reservas': reservas})

def eliminar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.delete()
    return redirect('mis_reservas')
