from django.http import HttpResponse

def client_list(request):
    return HttpResponse("Listado de clientes")

def client_add(request):
    return HttpResponse("Agregar cliente")

def client_edit_select(request):
    return HttpResponse("Seleccionar cliente a modificar")
