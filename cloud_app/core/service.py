import requests
from django.http import HttpResponse, QueryDict
from .models import VirtualMachine

class CheckService:
    possibility = False
    total = 0

    def __init__(self, request):
        self.possibility = check_configs(request)
        self.total = check_bill(request)


    def check_configs(self, request):
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
                        return True
        return False

        def check_bill(self, request):
            url = 'http://service_http:5000/price/' + request.META['QUERY_STRING']
            response = requests.get(url)
            print(response)
            print('check_balance fin')
            pass
