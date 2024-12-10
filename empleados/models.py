from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError


class TipoUsuario(models.TextChoices):
    coordinador = 'coordinador', 'coordinador'
    empleado = 'empleado', 'empleado'
    admin = 'admin', 'admin'


class UserManager(BaseUserManager):
    def create_user(self, cedula, password=None, **extra_fields):
        if not cedula:
            raise ValueError('Debe tener una cedula')
        user = self.model(cedula=cedula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cedula, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    cedula = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    apellido1 = models.CharField(max_length=255)
    apellido2 = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=20, choices=TipoUsuario.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['nombre', 'email', 'tipo_usuario', 'apellido1', 'apellido2']


class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField()
    turno = models.CharField(
        max_length=10,
        choices=[('mañana', 'Mañana'), ('tarde', 'Tarde')]
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def es_valida(self):
        """
        Verifica si la reserva es válida con base en la regla de descanso cada 2 meses.
        """
        dos_meses_atras = self.fecha - timedelta(days=60)
        reservas_previas = Reserva.objects.filter(
            usuario=self.usuario,
            fecha__gte=dos_meses_atras,
            fecha__lt=self.fecha
        )
        return not reservas_previas.exists()

    def __str__(self):
        return f'{self.usuario} - {self.fecha} ({self.turno})'




