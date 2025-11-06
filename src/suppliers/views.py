from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier
from .forms import SupplierForm

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/list.html", {"object_list": suppliers, "title": "Listado de Proveedores"})

def supplier_add(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("suppliers:list")
    else:
        form = SupplierForm()
    return render(request, "suppliers/add.html", {"form": form, "title": "Agregar Proveedor"})

def supplier_edit_select(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/edit_select.html", {"suppliers": suppliers, "title": "Seleccionar Proveedor"})
