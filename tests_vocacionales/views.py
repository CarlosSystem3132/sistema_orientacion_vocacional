from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pregunta, Respuesta, AreaVocacional, ResultadoTest
from .forms import TestVocacionalForm
from .logica_difusa import procesar_resultados
from reportes.utils import generar_reporte_pdf
from django.http import HttpResponse

@login_required
def test_vocacional(request):
    if request.method == 'POST':
        preguntas = Pregunta.objects.all()
        form = TestVocacionalForm(request.POST, preguntas=preguntas)
        if form.is_valid():
            for pregunta in preguntas:
                opcion_id = form.cleaned_data[f'pregunta_{pregunta.id}']
                Respuesta.objects.create(
                    usuario=request.user,
                    pregunta=pregunta,
                    opcion_id=opcion_id
                )
            return redirect('resultados')
    else:
        preguntas = Pregunta.objects.all()
        form = TestVocacionalForm(preguntas=preguntas)
    
    return render(request, 'tests_vocacionales/test.html', {'form': form})

@login_required
def resultados(request):
    respuestas = Respuesta.objects.filter(usuario=request.user).select_related('pregunta', 'opcion')
    
    # Preparar datos para la lógica difusa
    datos_respuestas = {}
    for respuesta in respuestas:
        tipo_test = respuesta.pregunta.tipo_test
        if tipo_test not in datos_respuestas:
            datos_respuestas[tipo_test] = {}
        
        area = respuesta.pregunta.area_vocacional.nombre
        if area not in datos_respuestas[tipo_test]:
            datos_respuestas[tipo_test][area] = []
        
        datos_respuestas[tipo_test][area].append(respuesta.opcion.valor)

    # Procesar resultados con lógica difusa
    resultados_difusos = procesar_resultados(datos_respuestas)

    # Guardar resultados
    for area, puntaje in resultados_difusos.items():
        area_vocacional = AreaVocacional.objects.get(nombre=area)
        ResultadoTest.objects.create(
            usuario=request.user,
            area_vocacional=area_vocacional,
            puntaje=puntaje
        )

    # Ordenar resultados
    resultados_ordenados = sorted(resultados_difusos.items(), key=lambda x: x[1], reverse=True)

    if request.GET.get('format') == 'pdf':
        pdf = generar_reporte_pdf(request.user, carreras_recomendadas)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=reporte_{request.user.username}.pdf'
        return response

    return render(request, 'tests_vocacionales/resultados.html', {'resultados': carreras_recomendadas})