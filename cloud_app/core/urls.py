from django.contrib import admin
from django.urls import path, include, reverse

from core import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.HomeListView.as_view(), name='home'),
    path('detail/<int:pk>', views.HomeDetailView.as_view(), name='detail'),
    path('edit', views.edit_page, name='edit_page'),
    path('new/', views.VirtualMachineCreateView.as_view(), name='vm_new'),
    path('login/', views.MyprojectLoginView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    # path('logout', views.MyProjectLogout.as_view(), name='logout_page'),
    path('check', views.check, name='check'),
]
