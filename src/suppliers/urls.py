from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('list/', views.supplier_list, name='list'),
    path('add/', views.supplier_add, name='add'),
    path('edit/', views.supplier_edit_select, name='edit_select'),
    path('edit/<int:supplier_id>/', views.supplier_edit, name='edit'),
]