from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.utils import timezone
from datetime import timedelta

class UnidadEducativa(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    es_administrador = models.BooleanField(default=False)
    unidad_educativa = models.ForeignKey(UnidadEducativa, on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    curso = models.CharField(max_length=50, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    codigo_qr = models.ImageField(upload_to='codigos_qr/', null=True, blank=True)
    fecha_generacion_qr = models.DateTimeField(null=True, blank=True)

    # Agregar related_name a los campos groups y user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='usuario_set',
        related_query_name='usuario'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario'
    )

    def generar_codigo_qr(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.username)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        self.codigo_qr.save(f'qr_{self.username}.png', File(buffer), save=False)
        self.fecha_generacion_qr = timezone.now()
        self.save()

    def codigo_qr_valido(self):
        if self.fecha_generacion_qr:
            return timezone.now() - self.fecha_generacion_qr <= timedelta(days=5)
        return False
