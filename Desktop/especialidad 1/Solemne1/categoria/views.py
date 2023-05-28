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
from prov.models import Proveedor
from categoria.models import Categoria
from .forms import CategoriaForm

#CATEGORIAS
@login_required
def agregar_categoria(request):
    data = {
        'form': CategoriaForm()
    }
    if request.method == 'POST':
        formulario = CategoriaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.INFO, 'Categoria creada!')
    return render(request, 'categoria/agregar_categoria.html',data)
    # profile = Profile.objects.get(user_id=request.user.id)
    # if profile.group_id != 1:
    #     messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
    #     return redirect('check_group_main')
    # template_name = 'ejemplos/agregar.html'
    # return render(request,template_name,{'profile':profile})
@login_required
def listar_categoria(request):
     categorias = Categoria.objects.all()
     data={
         'categoria': categorias
     }
     return render(request, 'categoria/listar_categoria.html',data)
@login_required
def modificar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    data ={
        'form': CategoriaForm(instance=categoria)
    }
    if request.method == 'POST':
        formulario = CategoriaForm(data=request.POST,instance=categoria)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_categoria")
    messages.add_message(request, messages.INFO, 'Categoria modificada!')
    return render(request, 'categoria/modificar_categoria.html',data)
@login_required
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.add_message(request, messages.INFO, 'Categoria eliminada!')
    return redirect(to="listar_categoria")



#########################
#CARGA MASIVA CATEGORIA
@login_required
def carga_masiva_categoria(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'categoria/carga_masiva_categoria.html'
    return render(request,template_name,{'profiles':profiles})

@login_required
def import_file_categoria(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre Categoria']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(1):
            if col_num == 0:
                ws.write(row_num, col_num, 'ej: categoria' , font_style)
    wb.save(response)
    return response  

@login_required
def categoria_carga_masiva_save(request):
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
            categoria_save = Categoria(
                nombre = nombre,                   
                )
            categoria_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron '+str(acc)+' registros')
        return redirect('carga_masiva_categoria')    
#####################################
