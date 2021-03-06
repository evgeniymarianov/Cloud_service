# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import csv
import json
with open('prices.csv') as f:
    prices = dict(csv.reader(f))
    for key, value in prices.items():
        prices[key] = int(value)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'
    print('!!!!!!!!!!!!!!!!!!!')


@app.route('/price/')
def price():
    params = {}
    for key in request.args:
        print('!!!!!!!!!!!!!!!!!!!')
        print(key)
        if key in ['hdd_type', 'os']:
            params[key] = request.args.getlist(key)[0]
        else:
        # if int(request.args.getlist(key)[0]) not in list(prices.keys()):
            # raise KeyError("U: 'cpu', 'ram', 'sata', 'sas', ssd'")
            params[key] = int(request.args.getlist(key)[0])
    cost = (params['cpu'] * prices['cpu']\
         + params['ram'] * prices['ram']\
	 + params['hdd_capacity'] * prices[params['hdd_type']])  * 0.01
         # + params['sata'] * prices['sata']) * 0.01
    # return "Стоимость заказа: " + str(cost) + " рублей"
    print(params)
    return json.dumps(cost)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
