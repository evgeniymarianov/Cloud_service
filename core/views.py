from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import VirtualMachine
from django.views.generic import ListView, DetailView
from .forms import VirtualMachineForm

def home(request):
    context = {
        'virtual_machines_list': VirtualMachine.objects.all().order_by('-id'),
        'form': VirtualMachineForm
        }
    return render(request, 'base.html', context)

def edit_page(request):
    template = 'edit_page.html'
    context = {
    'virtual_machines_list': VirtualMachine.objects.all().order_by('-id'),
    'form': VirtualMachineForm
    }
    return render(request, 'edit_page.html', context)

class HomeListView(ListView):
    model = VirtualMachine
    template_name = 'base.html'
    context_object_name = 'virtual_machines_list'
    form = VirtualMachineForm()


class HomeDetailView(DetailView):
    model = VirtualMachine
    template_name = 'detail.html'
    context_object_name = 'get_virtual_machine'
    form = VirtualMachineForm()
