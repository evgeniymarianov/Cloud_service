from rest_framework import serializers

from core.models import VirtualMachine


class VirtualMachineListSerializer(serializers.ModelSerializer):
    networks = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    class Meta:
        model = VirtualMachine
        fields = ("current_user", "ram", "cpu", "hdd_type", "hdd_capacity", "networks")


class VirtualMachineDetailSerializer(serializers.ModelSerializer):
    networks = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    current_user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = VirtualMachine
        fields = '__all__'
