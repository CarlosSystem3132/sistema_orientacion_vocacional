from django.test import TestCase
from django.urls import reverse
from .models import Usuario, UnidadEducativa

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.unidad_educativa = UnidadEducativa.objects.create(nombre="Test School", direccion="Test Address")
        self.usuario = Usuario.objects.create_user(username="testuser", password="testpass123", unidad_educativa=self.unidad_educativa)

    def test_registro_view(self):
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/registro.html')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertRedirects(response, reverse('perfil'))

    def test_perfil_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/perfil.html')