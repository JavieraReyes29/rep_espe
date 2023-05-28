import json
import pandas as pd
import xlwt
#nuevas importaciones 30-05-2022
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from registration.models import Profile

#fin nuevas importaciones 30-05-2022

from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Producto
from .forms import ProductoForm
from prov.models import Proveedor


@login_required
def ejemplos_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'product/ejemplos_main.html'
    return render(request,template_name,{'profile':profile})

#PRODUCTOS
@login_required
def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.INFO, 'Producto creado!')
    return render(request, 'product/agregar.html',data)

    # profile = Profile.objects.get(user_id=request.user.id)
    # if profile.group_id != 1:
    #     messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
    #     return redirect('check_group_main')
    # template_name = 'ejemplos/agregar.html'
    # return render(request,template_name,{'profile':profile})
@login_required
def listar_producto(request):
     productos = Producto.objects.all()
     data={
         'productos': productos
     }
     return render(request, 'product/listar.html',data)
@login_required
def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data ={
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST,instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_producto")
    messages.add_message(request, messages.INFO, 'Producto actualizado!')
    return render(request, 'product/modificar.html',data)
@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.add_message(request, messages.INFO, 'Producto eliminado!')
    return redirect(to="listar_producto")
#CARGA MASIVA PRODUCTO
@login_required
def ejemplos_carga_masiva(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'product/ejemplos_carga_masiva.html'
    return render(request,template_name,{'profiles':profiles})

@login_required
def import_file(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre Producto','Precio','Descripcion','Talla','Categoria']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(5):
            if col_num == 0:
                ws.write(row_num, col_num, 'ej: producto' , font_style)
            if col_num == 1:                           
                ws.write(row_num, col_num, '10000' , font_style)
            if col_num == 2:                           
                ws.write(row_num, col_num, 'Polera de diseñador...' , font_style)
            if col_num == 3:                           
                ws.write(row_num, col_num, 'xs,s,m,l,xl' , font_style)
            if col_num == 4:                           
                ws.write(row_num, col_num, '1,2,3...' , font_style)
    wb.save(response)
    return response  

@login_required
def ejemplos_carga_masiva_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        #try:
        print(request.FILES['myfile'])
        data = pd.read_excel(request.FILES['myfile'])
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            #capturamos los datos desde excel
            nombre = str(item[1])            
            precio = int(item[2])
            descripcion = str(item[3])            
            talla = str(item[4])
            categoria_id = str(item[5])
            producto_save = Producto(
                nombre = nombre,            
                precio = precio,
                descripcion = descripcion,            
                talla = talla,
                categoria_id = categoria_id,         
                
                )
            producto_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron '+str(acc)+' registros')
        return redirect('ejemplos_carga_masiva')    
#####################################