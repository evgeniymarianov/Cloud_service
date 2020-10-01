import requests
from django.http import HttpResponse, QueryDict
from .models import VirtualMachine, Report, User, AdditionalHdd
import json
import csv
from random import choice
from django.db.models import Sum


class CheckService:
    def __init__(self, request):
        self.balance_after_transaction = 0
        self.configuration_availability = False
        self.check_configs(request)
        self.check_bill(request)
        self.message(request)
        pass


    def check_configs(self, request):
        params =  QueryDict(request.META['QUERY_STRING'], mutable=True)
        url = 'http://possible_orders.srv.w55.ru/'
        possible_configs = requests.get(url).json()['specs']
        for k, v in params.items():
            params['cpu'] = int(params['cpu'])
            params['ram'] = int(params['ram'])
            params['hdd_capacity'] = int(params['hdd_capacity'])
            for config in possible_configs:
                if (params['cpu'] in config['cpu']) & (params['ram'] in config['ram']) & (params['hdd_type'] in config['hdd_type']) & (params['os'] in config['os']):
                    min = config['hdd_capacity'][params['hdd_type']]['from']
                    max = config['hdd_capacity'][params['hdd_type']]['to']
                    if min <= int(params['hdd_capacity']) <= max:
                        self.configuration_availability = True
        if self.configuration_availability:
            new_virtual_machine = VirtualMachine(
                cpu=params['cpu'],
                ram=params['ram'],
                hdd_type=params['hdd_type'],
                hdd_capacity=params['hdd_capacity'],
                current_user=request.user
            )
            new_virtual_machine.save()
            print("!!!!!!!!!!!!!!!!")
            print(new_virtual_machine.id)
            pass
        pass


    def check_bill(self, request):
        url = 'http://cost_service:5000/price/?' + request.META['QUERY_STRING']
        self.total_cost = round(requests.get(url).json(), 2)
        self.balance_after_transaction = request.user.balance - self.total_cost
        pass


    def message(self, request):
        data = {}
        if self.configuration_availability and (self.balance_after_transaction >= 0):
            data = {
                'answer': {
                    'result': True,
                    'total': self.total_cost,
                    'balance': request.user.balance,
                    'balance_after_transaction': self.balance_after_transaction,
                },
                'status': 'ok'
            }
        elif (self.configuration_availability == False) or (self.balance_after_transaction < 0):
            data = {
                'answer': {
                    'result': False,
                    'error': 'incorrect VM configuration or insufficient funds are used'
                },
                'status': 'not_acceptable'
            }
        elif (request.user == False) or (request.user.balance == False):
            data = {
                'answer': {
                    'result': False,
                    'error': 'the current session does not have a username or balance'
                },
                'status': 'unauthorized'
            }
        else:
            data = {
                'answer': {
                    'result': False,
                    'error': 'error accessing the external system'
                },
                'status': 'service_unavailable'
            }
        self.data = json.dumps(data)
        pass


class CreateDataService:
    """docstring for CreateDataService"""
    def __init__(self):
        data_path = '/data/csvs/'
        self.create_users()
        self.loaded_data = self.load_local_csv(data_path)
        self.create_virtual_machines(self.loaded_data)


    def load_local_csv(self, path):
        with open(str(path) + 'vms.csv') as f:
            virtual_machines_list = list(csv.reader(f))
            for vm in virtual_machines_list:
                for n in [0, 1, 2, 4]:
                    vm[n] =  int(vm[n])
            print(virtual_machines_list[:5])
        with open(str(path) + 'prices.csv') as f:
            price_list = dict(csv.reader(f))
        for key, value in price_list.items():
            if key in ['cpu', 'ram', 'hdd_capacity', 'ssd', 'sata', 'sas']:
                price_list[key] = int(value)
        with open(str(path) + 'volumes.csv') as f:
            additional_hdds_list = list(csv.reader(f))
            for hdd in additional_hdds_list:
                for n in [0, 2]:
                    hdd[n] =  int(hdd[n])
            print(additional_hdds_list[:5])
        loaded_data = {
            'vms': virtual_machines_list,
            'price_list': price_list,
            'add_hdds': additional_hdds_list
            }
        return loaded_data


    def create_users(self):
        new_user1 = User.objects.create(
            username = 'evgen1426',
            password = 'fgjt[fkb005]'
        )
        new_user2 = User.objects.create(
            username = 'evgen1427',
            password = 'fgjt[fkb005]'
        )
        pass


    def create_virtual_machines(self, loaded_data):
        price_list = loaded_data['price_list']
        for vm in loaded_data['vms']:
            new_vm = VirtualMachine.objects.create(
                csv_id = vm[0],
                ram = vm[1],
                cpu = vm[2],
                hdd_type = str(vm[3]),
                hdd_capacity = vm[4]
            )
            new_vm.current_user = choice(User.objects.all())
            new_vm.save()
        for hdd in loaded_data['add_hdds']:
            #print('hdd = ' + str(hdd))
            #print('VirtualMachine.objects.get(id=hdd[0]) = ' + str(VirtualMachine.objects.get(id=hdd[0])))
            new_hdd = AdditionalHdd.objects.create(
                virtual_machine = VirtualMachine.objects.get(csv_id=hdd[0]),
                csv_id = int(hdd[0]),
                hdd_type = str(hdd[1]),
                hdd_capacity = int(hdd[2])
            )
            new_hdd.cost = (new_hdd.hdd_capacity * price_list[new_hdd.hdd_type]) * 0.01
            new_hdd.save()
        vms = VirtualMachine.objects.all()
        for vm in vms:
            vm.cost = (vm.cpu * price_list['cpu'] + vm.ram * price_list['ram'] + vm.hdd_capacity * price_list[vm.hdd_type]) * 0.01
            vm.save()
            print('vm.csv_id = ' + str(vm.csv_id))
            print('vm.cost = ' + str(vm.cost))
            add_hdds = AdditionalHdd.objects.filter(virtual_machine=vm)
            print('HDDS' + str(add_hdds))
            for hdd in add_hdds:
                print(hdd.csv_id)
                vm.cost += hdd.cost
                vm.save()
                print('vm.csv_id2222222222 = ' + str(vm.csv_id))
                print('vm.NEW_cost = ' + str(vm.cost))
            vm.save()
        pass


def create_report(user_id):
    print('!!!!!!!!!!!!!!servicsssssssssssssssssss')
    user = User.objects.get(id=user_id)
    vms = VirtualMachine.objects.filter(current_user=user)
    print('!!!!!!!!!!!!!!service')
    # q = Report(text="It's ok?")
    # q.save()
    print(vms)
    print(q)
    pass


class CreateReportService:
    """docstring for CreateReportService"""
    def __init__(self):
        for user in User.objects.all():
            report = Report.objects.create(current_user = user)
            report.most_cheapest = self.most_cheapest(user)
            report.most_expensive = self.most_expensive(user)
            report.most_capacious = self.most_capacious(user, 'sata')
            report.most_additional_hdds_by_number = self.most_additional_hdds_by_number(user, 'sata')
            report.most_additional_hdds_by_capacity = self.most_additional_hdds_by_capacity(user, 'sata')
            print(report)
            #report.most_capacious = self.most_capacious(user.id)
            #report.most_additional_hdds_by_number = self.most_additional_hdds_by_number(user.id)
            #report.most_additional_hdds_by_capacity = self.most_additional_hdds_by_capacity(user.id)


    def most_cheapest(self, user):
        print('++++++++++++++++start most_cheapest')
        vms = VirtualMachine.objects.filter(current_user=user).order_by('-cost')[:5]
        text = ''
        for vm in vms:
            text += str(vm) + "\n"
        return text


    def most_expensive(self, user):
        print('000000000000000000000start most_expensive')
        vms = VirtualMachine.objects.filter(current_user=user).order_by('cost')[:5]
        text = ''
        for vm in vms:
            text += str(vm) + "\n"
        return text


    def most_capacious(self, user, type):
        vms = VirtualMachine.objects.filter(current_user=user)
        text = ''
        for vm in vms:
            vm.volume = 0
            if vm.hdd_type == type:
                vm.volume += vm.hdd_capacity
            for hdd in vm.additionalhdd_set.all():
                if hdd.hdd_type == type:
                    vm.volume += hdd.hdd_capacity
            text += 'CSV_ID = ' + str(vm.csv_id) + '   VOLUME = ' + str(vm.volume) + "\n"
        return text


    def most_additional_hdds_by_number(self, user, type):
        vms = VirtualMachine.objects.filter(current_user=user)
        text = ''
        for vm in vms:
            vm.num_of_hdd = vm.additionalhdd_set.filter(hdd_type=type).count()
            text += 'CSV_ID = ' + str(vm.csv_id) + '   NUM_OF_HDD = ' + str(vm.num_of_hdd) + "\n"
        return text


    def most_additional_hdds_by_capacity(self, user, type):
        vms = VirtualMachine.objects.filter(current_user=user)
        text = ''
        for vm in vms:
            vm.capacity_of_type = vm.additionalhdd_set.filter(hdd_type=type).aggregate(Sum('hdd_capacity'))['hdd_capacity__sum']
            text += 'CSV_ID = ' + str(vm.csv_id) + '   CAPACITY_OF_HDD = ' + str(vm.capacity_of_type) + "\n"
        return text
