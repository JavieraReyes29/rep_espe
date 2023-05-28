from django.shortcuts import render
from product.models import Producto
from cotizacion.models import Cotizacion,ItemCot
from gestioncliente.models import Cliente
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from registration.models import Profile
from datetime import date
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import TableStyle
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph





# Create your views here.


def crear_cotizacion(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        producto_id = request.POST.get('producto')
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get('cantidad'))
        descripcion = request.POST.get('descripcion')
        fecha = date.today()
        orden_cotizacion = Cotizacion.objects.create(cliente=cliente,fecha=fecha)
        orden_cotizacion.save()
        item = ItemCot.objects.create(orden_cotizacion=orden_cotizacion, producto=producto, cantidad=cantidad,descripcion=descripcion)
        item.save() 
        return redirect('ver_cotizacion', orden_id=orden_cotizacion.id)
    clientes = Cliente.objects.all() 
    productos = Producto.objects.all()
    return render(request, 'crear_cotizacion.html', {'clientes': clientes, 'productos': productos})


def ver_cotizacion(request, orden_id):
    orden = get_object_or_404(Cotizacion, id=orden_id)
    return render(request, 'ver_cotizacion.html', {'orden': orden})


def eliminar_cotizacion(request, orden_id):
    orden = get_object_or_404(Cotizacion, id=orden_id)
    orden.delete()
    return redirect('listar_cotizacion')

def listar_cotizacion(request):
    ordenes = Cotizacion.objects.all()
    return render(request, 'listar_cotizacion.html', {'ordenes': ordenes})


def ola(request, orden_id):
    if request.method == 'POST':
        orden = get_object_or_404(Cotizacion, id=orden_id)
        print("alo")
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        producto = get_object_or_404(Producto, id=producto_id)
        print("XD")
        item = ItemCot.objects.create(orden_cotizacion=orden, producto=producto, cantidad=cantidad)
        return redirect('ver_cotizacion', orden_id=orden.id)
    else:
        orden = get_object_or_404(Cotizacion, id=orden_id)
        print("LLEGA ACA")
        productos = Producto.objects.all()
        return render(request, 'ola.html', {'orden': orden, 'productos': productos})
    

def eliminar(request, item_id):
    item = get_object_or_404(ItemCot, id=item_id)
    orden_id = item.orden_cotizacion.id
    item.delete()
    return redirect('ver_cotizacion', orden_id=orden_id)


def eliminar_producto(request, cotizacion_id, producto_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    producto = get_object_or_404(ItemCot, id=producto_id, cotizacion=cotizacion)

    if request.method == 'POST':
        producto.delete()
        return redirect('ver_cotizacion', cotizacion_id=cotizacion.id)

    return render(request, 'eliminar_producto.html', {'cotizacion': cotizacion, 'producto': producto})


def cotizacion_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'cotizacion_main.html'
    return render(request,template_name,{'profile':profile})


def generar_reporte_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_cotizaciones.pdf"'

    document = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    style_table = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#EEEEEE'),
    ])
    style_paragraph = ParagraphStyle(
        name='BodyText',
        parent=styles['Normal'],
        spaceBefore=6,
        spaceAfter=6,
    )

    data = [['ID', 'Cliente','Cantidad', 'Productos', 'Total']]
    for cotizacion in cotizaciones:
        productos = [f"{item.producto.nombre} ({item.cantidad}) " for item in cotizacion.items.all()]
        productos_str = ", ".join(productos)
        data.append([str(cotizacion.id), str(cotizacion.cliente), productos_str, str(cotizacion.calcular_total())])

    table = Table(data)
    table.setStyle(style_table)

    elements.append(Paragraph('Informe de Cotizaciones', styles['Heading1']))
    elements.append(Paragraph('Fecha: ' + date.today().strftime('%d/%m/%Y'), style_paragraph))
    elements.append(Paragraph('Listado de cotizaciones:', styles['Heading3']))
    elements.append(table)

    document.build(elements)

    return response