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
from .forms import ProveedorForm

@login_required
def proveedor_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'prov/proveedor_main.html'
    return render(request,template_name,{'profile':profile})
@login_required
def agregar_proveedor(request):
    data = {
        'form': ProveedorForm()
    }
    if request.method == 'POST':
        formulario = ProveedorForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.INFO, 'Proveedor creado!')
    return render(request, 'prov/agregar_proveedor.html',data)
@login_required
def listar_proveedor(request):
     proveedor = Proveedor.objects.all()
     data={
         'proveedor': proveedor
     }
     return render(request, 'prov/listar_proveedor.html',data)
@login_required
def actualizar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    data ={
        'form': ProveedorForm(instance=proveedor)
    }
    if request.method == 'POST':
        formulario = ProveedorForm(data=request.POST,instance=proveedor)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_proveedor")
    messages.add_message(request, messages.INFO, 'proveedor actualizado!')
    return render(request, 'prov/actualizar_proveedor.html',data)

@login_required
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)

    proveedor.delete()
    messages.add_message(request, messages.INFO, 'proveedor eliminado!')
    return redirect(to="listar_proveedor")