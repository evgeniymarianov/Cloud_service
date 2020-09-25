import requests
from django.http import HttpResponse, QueryDict
from .models import VirtualMachine, Report, User, AdditionalHdd
import json
import csv


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


def load_local_csv(path):
    with open(str(path) + 'vms.csv') as f:
        vms_csv = list(csv.reader(f))
        print(vms_csv[:5])

    with open(str(path) + 'prices.csv') as f:
        prices = dict(csv.reader(f))
        print(prices)

    for key, value in prices.items():
        if key in ['cpu', 'ram', 'hdd_capacity', 'ssd', 'sata', 'sas']:
            prices[key] = int(value)

    with open(str(path) + 'volumes.csv') as f:
        vms_volumes = list(csv.reader(f))

    ## for vm in vms_csv:
    ##     new_virtual_machine = VirtualMachine(
    ##         ram = int
    ##     )


def create_report(user_id):
    print('!!!!!!!!!!!!!!servicsssssssssssssssssss')
    user = User.objects.get(id=user_id)
    vms = VirtualMachine.objects.filter(current_user=user)
    print('!!!!!!!!!!!!!!service')
    q = Report(text="It's ok?")
    q.save()
    print(vms)
    print(q)
    pass
