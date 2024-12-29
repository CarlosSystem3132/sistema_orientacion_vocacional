from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from tests_vocacionales.models import ResultadoTest
from .forms import SolicitudReporteForm

@login_required
def solicitar_reporte(request):
    if request.method == 'POST':
        form = SolicitudReporteForm(request.POST)
        if form.is_valid():
            return generar_reporte_pdf(request.user)
    else:
        form = SolicitudReporteForm()
    return render(request, 'reportes/solicitar_reporte.html', {'form': form})

def generar_reporte_pdf(usuario):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Reporte de Orientación Vocacional para {usuario.get_full_name()}", styles['Title']))
    elements.append(Spacer(1, 12))

    # Información del usuario
    elements.append(Paragraph(f"Nombre: {usuario.get_full_name()}", styles['Normal']))
    elements.append(Paragraph(f"Edad: {usuario.edad}", styles['Normal']))
    elements.append(Paragraph(f"Curso: {usuario.curso}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Resultados del test
    resultados = ResultadoTest.objects.filter(usuario=usuario).order_by('-puntaje')[:3]
    data = [['Área Vocacional', 'Puntaje']]
    for resultado in resultados:
        data.append([resultado.area_vocacional.nombre, f"{resultado.puntaje:.2f}"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Descripción de las áreas vocacionales recomendadas
    for resultado in resultados:
        elements.append(Paragraph(f"{resultado.area_vocacional.nombre}", styles['Heading2']))
        elements.append(Paragraph(resultado.area_vocacional.descripcion, styles['Normal']))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=reporte_{usuario.username}.pdf'
    response.write(pdf)
    return response

