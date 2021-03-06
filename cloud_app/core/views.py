from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import VirtualMachine, User, Report
from django.views.generic import ListView, DetailView, CreateView
from .forms import VirtualMachineForm, RegisterUserForm, AuthUserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from .service import CheckService, create_report
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.contrib import messages


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


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
    print(request.GET.get("cpu", "what?"))
    print("!!!!!!!!!!!!!!!!")
    print(current_user())
    check_service = CheckService(request)
    # return render(request, 'base.html')
    return HttpResponse(check_service.data)

#def report(request):
    #user_id = request.user.id
    #print(user_id)
    #create_report_task.delay(user_id)
    #return HttpResponse('OKey')

class MyprojectLoginView(LoginView):
    model = VirtualMachine
    template_name = 'login.html'
    context_object_name = 'virtual_machines_list'
    success_url = reverse_lazy('home')

class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('edit_page')

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

class VirtualMachineCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView): # новое изменение
    login_url = reverse_lazy('login_page')
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
