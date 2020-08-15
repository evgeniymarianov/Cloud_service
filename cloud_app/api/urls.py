from django.urls import path

from . import views


urlpatterns = [
    path("vm/", views.VirtualMachineListView.as_view()),
]
