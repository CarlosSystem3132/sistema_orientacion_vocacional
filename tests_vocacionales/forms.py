from django import forms
from .models import Pregunta, Opcion

class TestVocacionalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        preguntas = kwargs.pop('preguntas', None)
        super(TestVocacionalForm, self).__init__(*args, **kwargs)
        
        if preguntas:
            for pregunta in preguntas:
                opciones = [(opcion.id, opcion.texto) for opcion in pregunta.opciones.all()]
                self.fields[f'pregunta_{pregunta.id}'] = forms.ChoiceField(
                    label=pregunta.texto,
                    choices=opciones,
                    widget=forms.RadioSelect,
                    required=True
                )