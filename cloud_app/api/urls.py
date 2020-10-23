from django.urls import path

from . import views


urlpatterns = [
    path("vm/", views.VirtualMachineListView.as_view()),
    path("vm/<int:pk>/", views.VirtualMachineDetailView.as_view()),
    path("user/<int:pk>/", views.UserDetailView.as_view()),
]
