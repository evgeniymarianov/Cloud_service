import requests
from django.http import HttpResponse, QueryDict
from .models import VirtualMachine
import json

class CheckService:
    def __init__(self, request):
        self.balance_after_transaction = 0
        self.conf_possobility = False
        self.data = 0
        #if self.check_configs(request):
        self.check_configs(request)
        print('check_configs ok')
        self.check_bill(request)
        print('check_bill ok')
        self.message(request)
        pass


    def check_configs(self, request):
        print('check_configs!!!!!!!!!!!!!!!!!')
        params =  QueryDict(request.META['QUERY_STRING'], mutable=True)
        print(params)
        url = 'http://possible_orders.srv.w55.ru/'
        possible_configs = requests.get(url).json()['specs']
        print(possible_configs)
        print("!!!!!!!!!!!!!!!!")
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
                        print('succ')
                        self.conf_possobility = True
                        pass
        pass


    def check_bill(self, request):
        print('check_bill!!!!!!!!!!!!!!!!!')
        url = 'http://cost_service:5000/price/?' + request.META['QUERY_STRING']
        self.total_cost = requests.get(url).json()
        # print(str(response) + str('>>>>>>>>>>>>>>>response'))
        print('check_balance fin')
        self.balance_after_transaction = request.user.balance - self.total_cost
        print(str(self.balance_after_transaction) + '---------balance_after_transaction')
        pass


    def message(self, request):
        print(self.balance_after_transaction)
        print(self.conf_possobility)
        data = {}
        if self.conf_possobility and (self.balance_after_transaction > 0):
            data = {
                'answer': {
                    'result': True,
                    'total': self.total_cost,
                    'balance': request.user.balance,
                    'balance_after_transaction': self.balance_after_transaction,
                },
                'status': 'ok'
            }
        self.data = json.dumps(data)
        pass
