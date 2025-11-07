from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Client
from .forms import ClientForm
from django.views.decorators.http import require_POST

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/list.html', {
        'object_list': clients,
        'title': 'Listado de Clientes',
        'model_name': 'client'
    })

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

def client_edit(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients:list')  # o donde quieras redirigir luego de guardar
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/edit.html', {
        'form': form,
        'title': 'Modificar Cliente'
    })

def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/detail.html', {
        'entity': client,
        'title': 'Detalle de Cliente',
        'edit_url': reverse('clients:edit', args=[client.id]),
        'delete_url': reverse('clients:delete', args=[client.id])
    })

@require_POST
def client_delete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return redirect('clients:list')