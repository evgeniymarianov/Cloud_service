from django import forms
from .models import VirtualMachine

class VirtualMachineForm(forms.ModelForm):
    class Meta:
        model = VirtualMachine
        fields = '__all__'
