import sys
import os
import socket
import threading
import random
import time
from EnvInterface import IEnvironment
import os
import psycopg2
import requests
from requests.auth import HTTPBasicAuth


sensor_id = 2


def start_simulation(environment):
    environment.run_simulation()


def get_authorization_key():
    login = {'email': 'root@email.com', 'password': '2wsxcde3'}
    resp = requests.post("https://inzynierka-server.herokuapp.com/api/auth/jwt/create/", json=login)
    headers = {'Authorization': 'Bearer ' + format(resp.json()['access'])}
    return headers


def write_humidity(environment, headers):
    json = {'measure_value': round(environment.get_humidity(), 3), 'measuring_device': sensor_id}
    resp = requests.post("https://inzynierka-server.herokuapp.com/api/daily-measurements/", json=json, headers=headers)
    if resp.status_code == 201:
        return 0
    else:
        return -1


def simulation_loop(environment, headers):
    status = write_humidity(environment, headers)
    if status == -1:
        print("An error occurred while writing humidity")
    time.sleep(60)


def main():
    environment = IEnvironment()
    headers = get_authorization_key()
    simulation_thread = threading.Thread(target=start_simulation, args=[environment])
    simulation_thread.daemon = True
    simulation_thread.start()

    while True:
        simulation_loop(environment, headers)


if __name__ == "__main__":
    main()