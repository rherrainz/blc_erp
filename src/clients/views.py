from django.shortcuts import render, get_object_or_404, redirect
from .models import Client
from .forms import ClientForm

def client_list(request):
    clients = Client.objects.all()
    return render(request, "clients/list.html", {"object_list": clients, "title": "Listado de Clientes"})

def client_add(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("clients:list")
    else:
        form = ClientForm()
    return render(request, "clients/add.html", {"form": form, "title": "Agregar Cliente"})

def client_edit_select(request):
    clients = Client.objects.all()
    return render(request, "clients/edit_select.html", {"clients": clients, "title": "Seleccionar Cliente"})
