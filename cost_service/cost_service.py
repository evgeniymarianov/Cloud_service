# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import csv
with open('prices.csv') as f:
    prices = dict(csv.reader(f))
    for key, value in prices.items():
        prices[key] = int(value)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/price/')
def price():
    params = {}
    for key in request.args:
        # if int(request.args.getlist(key)[0]) not in list(prices.keys()):
            # raise KeyError("U: 'cpu', 'ram', 'sata', 'sas', ssd'")
        params[key] = int(request.args.getlist(key)[0])
    cost = (params['cpu'] * prices['cpu']\
         + params['ram'] * prices['ram']\
         + params['ssd'] * prices['ssd']\
         + params['sata'] * prices['sata']\
         + params['sas'] * prices['sas']) * 0.01
    return "Стоимость заказа: " + str(cost) + " рублей"


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
