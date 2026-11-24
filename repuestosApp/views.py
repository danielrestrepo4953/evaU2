from asyncio.log import logger

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

from repuestosApp.models import repuestos, descripcion
from .forms import RepuestoForm

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER

@login_required
def inicio(request):
    repuesto = repuestos.objects.all()
    return render(request, 'repuestos/repuestos/inicio.html', {'repuestos': repuesto})

@login_required
def detalle_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(repuestos, id=repuesto_id)
    detalle = descripcion.objects.filter(repuesto_id=repuesto_id).first()
    return render(
        request,
        'repuestos/repuestos/usuario.html',
        {'repuesto': repuesto, 'detalle': detalle}
    )


@login_required
def crear_repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El repuesto se registró correctamente.')
            return redirect('home_repuestos')
    else:
        form = RepuestoForm()

    return render(request, 'repuestos/repuestos/formulario.html', {'form': form})


@login_required
def editar_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(repuestos, id=repuesto_id)
    if request.method == 'POST':
        form = RepuestoForm(request.POST, request.FILES, instance=repuesto)
        if form.is_valid():
            form.save()
            messages.success(request, 'El repuesto se actualizó correctamente.')
            return redirect('home_repuestos')
    else:
        form = RepuestoForm(instance=repuesto)

    return render(request, 'repuestos/repuestos/formulario.html', {
        'form': form,
        'repuesto': repuesto,
    })


@login_required
def eliminar_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(repuestos, id=repuesto_id)
    if request.method == 'POST':
        repuesto.delete()
        messages.success(request, 'El repuesto se eliminó correctamente.')
        return redirect('home_repuestos')

    return render(request, 'repuestos/repuestos/eliminar.html', {'repuesto': repuesto})



def exportar_repuestos_excel(request):
    # Obtener todos los repuestos de la base de datos
    lista_repuestos = repuestos.objects.all()
    # Contexto de los repuestos
    context = {'repuestos': lista_repuestos}
    # libro de trabajo de Excel
    wb = Workbook()
    # hoja activa
    ws = wb.active
    # Titulo
    ws.title = "Repuestos"
    # Encabezados de las columnas
    ws.append(['codigo', 'nombre', 'detalle', 'precio', 'stock'])
    # Datos de los repuestos
    for repuesto in lista_repuestos:
        ws.append([repuesto.codigo,
                    repuesto.nombre,
                    repuesto.detalle,
                    repuesto.precio,
                    repuesto.stock])
    # Devolver archivo Excel como repuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['content-Disposition'] = 'attachment; filename="repuestos.xlsx"'
    # Guardar libro de trabajo en la repuesta
    wb.save(response)
    return response


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.page_num = 0
    def showPage(self):
        self.page_num += 1
        self._draw_footer()
        canvas.Canvas.showPage(self)
    def save(self):
        canvas.Canvas.save(self)
    def _draw_footer(self):
        self.saveState()
        self.setLineWidth(1)
        self.line(0.5*inch, 0.6*inch, 7.5*inch, 0.6*inch)
        self.setFont('Helvetica', 8)
        self.drawString(0.5*inch, 0.3*inch, f"Pagina {self.page_num} de {self._pageNumber}")
        self.drawString(7.2*inch, 0.3*inch, " 2026 - Taller de Reparaciones")
        self.restoreState()

def exportar_repuestos_pdf(request):
    from django.conf import settings
    import os
    response = HttpResponse(content_type= 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename="repuestos.pdf"'
    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.6*inch
    )
    elementos = []
    styles = getSampleStyleSheet()
    header_sytele = ParagraphStyle(
        'HeaderCustom',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=0.1*inch
    )
    header_empresa_style = ParagraphStyle(
        'HeaderEmpresa',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#1f885c"),
        spaceAfter=0.05*inch
    )
    titulo_style = ParagraphStyle(
        'TituloCustom',
        parent=styles['Heading1'],
        fontSize= 20,
        textColor= colors.HexColor('#1f4788'),
        spaceAfter= 0.2*inch,
        alignment= TA_CENTER,
        fontName= 'Helvetica-Bold'
    )
    from datetime import datetime
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    encabezado = Paragraph("REPORTE DE REPUESTOS", header_empresa_style)
    elementos.append(encabezado)
    empresa_info = Paragraph("Empresa: Negocio de Reparaciones", header_empresa_style)
    elementos.append(empresa_info)
    fecha_info = Paragraph(f"Fecha: {fecha_actual}", header_empresa_style)
    elementos.append(fecha_info)
    elementos.append(Spacer(1, 0.15*inch))
    try:
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
        if os.path.exists(logo_path):
            logo =Image(logo_path, wid=0.8*inch, height=0.8*inch)
            elementos.append(logo)
            elementos.append(Spacer(1, 0.1*inch))
    except Exception as e:
        logger.warning(f"No se pudo cargar el logo: {e}")
    titulo = Paragraph("Reporte de repuestos", titulo_style)
    elementos.append(titulo)
    elementos.append(Spacer(1, 0.2*inch))
    encabezado = ['Codigo', 'Nombre', 'Detalle', 'Precio', 'Stock']
    datos = []
    lista_repuestos = repuestos.objects.all()
    for repuesto in lista_repuestos:
        datos.append([repuesto.codigo, repuesto.nombre, repuesto.detalle, str(repuesto.precio), str(repuesto.stock)])
    tabla = Table([encabezado] + datos,
                    colWidths=[1.25*inch, 1.75*inch, 2.5*inch, 1*inch, 1*inch])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f2f2f2')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elementos.append(tabla)
    doc.build(elementos, canvasmaker=NumberedCanvas)
    return response