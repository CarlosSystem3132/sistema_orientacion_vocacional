from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors
from io import BytesIO

def generar_reporte_pdf(usuario, resultados):
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

    # Gráfico de resultados
    drawing = Drawing(400, 200)
    data = [resultado[1] for resultado in resultados]
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = [data]
    bc.categoryAxis.categoryNames = [resultado[0] for resultado in resultados]
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 10
    bc.bars[0].fillColor = colors.blue
    drawing.add(bc)

    elements.append(drawing)
    elements.append(Spacer(1, 12))

    # Descripción de las carreras recomendadas
    for carrera, puntaje in resultados:
        elements.append(Paragraph(f"{carrera}: {puntaje:.2f}%", styles['Heading2']))
        elements.append(Paragraph("Descripción de la carrera...", styles['Normal']))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf