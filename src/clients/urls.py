from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('list/', views.client_list, name='list'),
    path('add/', views.client_add, name='add'),
    path('edit_select/', views.client_edit_select, name='edit_select'),
    path('edit/<int:client_id>/', views.client_edit, name='edit'),       
]