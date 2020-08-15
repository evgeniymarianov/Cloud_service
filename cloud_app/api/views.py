from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import VirtualMachineListSerializer, VirtualMachineDetailSerializer
from core.models import VirtualMachine

class VirtualMachineListView(APIView):
    def get(self, request):
        virtual_machines = VirtualMachine.objects.all()
        serializer = VirtualMachineListSerializer(virtual_machines, many=True)
        return Response(serializer.data)


class VirtualMachineDetailView(APIView):
    def get(self, request, pk):
        virtual_machine = VirtualMachine.objects.get(id=pk)
        serializer = VirtualMachineDetailSerializer(virtual_machine)
        return Response(serializer.data)
