from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import RegistroForm, LoginForm
from .models import Usuario, UnidadEducativa
import qrcode
from io import BytesIO
from django.core.files import File

def inicio(request):
    return render(request, 'usuarios/inicio.html')

def nosotros(request):
    return render(request, 'usuarios/nosotros.html')

def contacto(request):
    return render(request, 'usuarios/contacto.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save(commit=False)
            codigo_qr = request.POST.get('codigo_qr')
            if codigo_qr:
                try:
                    admin = Usuario.objects.get(codigo_qr=codigo_qr, es_administrador=True)
                    if admin.codigo_qr_valido():
                        usuario.unidad_educativa = admin.unidad_educativa
                        usuario.save()
                        login(request, usuario)
                        return redirect('perfil')
                    else:
                        form.add_error('codigo_qr', 'El código QR ha expirado.')
                except Usuario.DoesNotExist:
                    form.add_error('codigo_qr', 'Código QR inválido.')
            else:
                form.add_error('codigo_qr', 'Se requiere un código QR válido para el registro.')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('perfil')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html')

@login_required
def generar_codigo_qr(request):
    if request.user.es_administrador:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(request.user.username)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        request.user.codigo_qr.save(f'qr_{request.user.username}.png', File(buffer), save=True)
        request.user.fecha_generacion_qr = timezone.now()
        request.user.save()
        return redirect('perfil')
    return redirect('inicio')

@login_required
def administracion(request):
    if request.user.es_administrador:
        unidades_educativas = UnidadEducativa.objects.all()
        return render(request, 'usuarios/administracion.html', {'unidades_educativas': unidades_educativas})
    return redirect('inicio')