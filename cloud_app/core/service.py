import requests
from django.http import HttpResponse, QueryDict
from .models import VirtualMachine
import json

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
                        new_virtual_machine = VirtualMachine(cpu=params['cpu'], ram=params['ram'], hdd_type=params['hdd_type'], hdd_capacity=params['hdd_capacity'])
                        new_virtual_machine.save()
                        self.configuration_availability = True
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
