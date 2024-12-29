from django.db import models
from usuarios.models import Usuario

class AreaVocacional(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    TIPOS_TEST = (
        ('holland', 'Holland'),
        ('kuder', 'Kuder'),
    )
    texto = models.CharField(max_length=500)
    tipo_test = models.CharField(max_length=20, choices=TIPOS_TEST)
    area_vocacional = models.ForeignKey(AreaVocacional, on_delete=models.CASCADE, related_name='preguntas')

    def __str__(self):
        return f"{self.get_tipo_test_display()}: {self.texto}"

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=200)
    valor = models.IntegerField()

    def __str__(self):
        return self.texto

class Respuesta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.username} - {self.pregunta.texto}: {self.opcion.texto}"

class ResultadoTest(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    area_vocacional = models.ForeignKey(AreaVocacional, on_delete=models.CASCADE)
    puntaje = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.area_vocacional.nombre}: {self.puntaje}"



class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre