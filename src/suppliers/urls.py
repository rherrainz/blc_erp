from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('list/', views.client_list, name='list'),
    path('add/', views.client_add, name='add'),
    path('edit/', views.client_edit_select, name='edit_select'),
]