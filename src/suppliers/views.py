from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Supplier
from .forms import SupplierForm

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/list.html', {
        'object_list': suppliers,
        'title': 'Listado de Proveedores',
        'model_name': 'supplier'
    })

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

def supplier_edit(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers:list')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'suppliers/edit.html', {
        'form': form,
        'title': 'Modificar Proveedor'
    })

def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    return render(request, 'suppliers/detail.html', {
        'entity': supplier,
        'title': 'Detalle de Proveedor',
        'edit_url': reverse('suppliers:edit', args=[supplier.id]),
        'delete_url': reverse('suppliers:delete', args=[supplier.id])
    })

@require_POST
def supplier_delete(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.delete()
    return redirect('suppliers:list')
