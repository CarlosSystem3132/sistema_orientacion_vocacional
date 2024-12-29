from django import forms

class SolicitudReporteForm(forms.Form):
    confirmar = forms.BooleanField(
        required=True,
        label="Confirmo que deseo generar mi reporte de orientación vocacional",
        help_text="Al marcar esta casilla, se generará un PDF con tus resultados."
    )

