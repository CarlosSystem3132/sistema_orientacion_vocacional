from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class RegistroForm(UserCreationForm):
    codigo_qr = forms.CharField(max_length=100, required=True)
    captcha = ReCaptchaField()

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'foto', 'curso', 'edad', 'codigo_qr']
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()