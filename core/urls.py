from django.contrib import admin
from django.urls import path, include, reverse

from core import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.HomeListView.as_view(), name='home'),
    path('detail/<int:pk>', views.HomeDetailView.as_view(), name='detail'),
    path('edit', views.edit_page, name='edit_page'),
    path('new/', views.VirtualMachineCreateView.as_view(), name='vm_new'),
]
