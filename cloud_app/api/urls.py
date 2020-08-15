from django.urls import path

from . import views


urlpatterns = [
    path("vm/", views.VirtualMachineListView.as_view()),
    path("vm/<int:pk>/", views.VirtualMachineDetailView.as_view()),
]
