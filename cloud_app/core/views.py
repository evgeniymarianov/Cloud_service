from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import VirtualMachine, User
from django.views.generic import ListView, DetailView, CreateView
from .forms import VirtualMachineForm, RegisterUserForm, AuthUserForm
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from .service import CheckService
# from django.contrib.auth.mixins import LoginRequiredMixin
import requests

def home(request):
    context = {
        'virtual_machines_list': VirtualMachine.objects.all().order_by('-id'),
        'form': VirtualMachineForm
        }
    return render(request, 'base.html', context)

def edit_page(request):
    success = False
    if request.method == 'POST':
        form = VirtualMachineForm(request.post)
        if form.is_valid():
            form.save()
            success = True
    template = 'edit_page.html'
    context = {
    'virtual_machines_list': VirtualMachine.objects.all().order_by('-id'),
    'form': VirtualMachineForm,
    'success': success
    }
    return render(request, 'edit_page.html', context)

def check(request):
    if not request.user.is_authenticated:
        return HttpResponse("You are no Authenticated")
    print(request.GET.get("cpu", "what?"))
    print("!!!!!!!!!!!!!!!!")
    check_service = CheckService(request)

#class Check(View):

    #def get(self, request):
        #return render(request, )

class MyprojectLoginView(LoginView):
    model = VirtualMachine
    template_name = 'login.html'
    context_object_name = 'virtual_machines_list'
    success_url = reverse_lazy('home')


class RegisterUserView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    success_msg = 'Пользователь успешно создан'

class HomeListView(ListView):
    model = VirtualMachine
    template_name = 'base.html'
    context_object_name = 'virtual_machines_list'
    form = VirtualMachineForm()


class HomeDetailView(DetailView):
    model = VirtualMachine
    template_name = 'detail.html'
    context_object_name = 'get_virtual_machine'
    # form = VirtualMachineForm()

class VirtualMachineCreateView(CreateView): # новое изменение
    model = VirtualMachine
    template_name = 'virtual_machine_new.html'
    fields = ['cpu', 'ram', 'hdd_type', 'hdd_capacity']
    success_url = reverse_lazy('home')
    success_msg = 'Заказ создан'
    def get_context_data(self, **kwargs):
        kwargs['virtual_machines_list'] = VirtualMachine.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.current_user = self.request.user
        self.object.save()
        return super().form_valid(form)
