from rest_framework import serializers

from core.models import VirtualMachine


class VirtualMachineListSerializer(serializers.ModelSerializer):

    class Meta:
        model = VirtualMachine
        fields = ("current_user", "ram", "cpu", "hdd_type", "hdd_capacity")
