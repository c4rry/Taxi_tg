# -*- coding: utf-8 -*-
import csv
import requests
from time import sleep
from datetime import datetime, date, time

def read_f(name):
    with open(name) as f:
        data = f.readlines()
        return data

def write_csv(data):
    #print("Writing data in csv file...")
    with open('rides.csv', 'w') as resultFile:
        order = ["driver_id", "driver_name", "collected_from_client", "cost_for_driver", "driver_tips",
                 "cost_for_driver_wo_tips", 'fact_ride_estimate', 'ended_at', 'origin_full_address',
                 'destination_full_address']
        wr = csv.DictWriter(resultFile, fieldnames=order, delimiter=';')
        wr.writeheader()
        for ride in data:
            wr.writerow(ride)


def get_response(start,finish):
    print(start, finish)
    url = 'https://gettpartner.ru/api/fleet/v1/auth'

    user = 'XXXXX@user.api' #user берется из ЛК Gett
    password = 'XXXXX' # пароль берется из ЛК Gett

    get_url = 'https://gettpartner.ru/api/fleet/v1/auth'
    response = requests.get(get_url, params={'login': user, 'password': password})
    access_token = str(response.json()['access_token'])
    hed = {'Authorization': 'Bearer ' + access_token}
    print(access_token)
    sleep(1)

    post_url = 'https://gettpartner.ru/api/fleet/v1/dbr/create'
    response = requests.post(post_url, headers=hed, json={'from': str(start), 'to': str(finish)})
    uid = str(response.json()['uid'])
    sleep(20)

    hed = {'Authorization': 'Bearer ' + access_token}
    post_url = 'https://gettpartner.ru/api/fleet/v1/dbr/get'
    data = {'uid': uid}
    flag = True
    while flag:
        response = requests.post(post_url, headers=hed, json=data)
        if str(response.json()['result']) == 'True':
            data = (response.json()['data']['rides'])
            break
        sleep(59)
    return data

def gett(start, finish):

    data = get_response(start, finish)
    drivers = dict()
    for ride in data:
        for key in ['coupon', 'distance', 'action_summ', 'payment_type', 'pwg_reward', 'division',
                    'scheduled_at', 'full_tips', 'order_id', 'parking_cost', 'driver_order_balance',
                    'recorded_waiting_time']:
            ride.pop(key)

        if ride['driver_name'] not in drivers.keys():
            drivers.update({ride['driver_name']: float(ride['cost_for_driver_wo_tips'])})
        else:
            drivers[ride['driver_name']] += float(ride['cost_for_driver_wo_tips'])

    with open('summary.txt', 'w') as resultFile:
        for driver, total in drivers.items():
            s = '{} заработал по Gett {} рублей (комиссия 20% учтена)\n'.format(driver, (total*0.8))
            resultFile.write(s)
    write_csv(data)

