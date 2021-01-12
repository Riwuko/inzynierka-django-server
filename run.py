from bh1750 import readLight
import requests
import time
from light import LightController

LIGHT_SENSOR_ID = 3
BULB_IP = "192.168.1.96"
BULB_ID = 2


def save_daily_average(headers):
    resp = requests.get("https://inzynierka-server.herokuapp.com/api/daily-measurements/1/reset/", headers=headers)
    if resp == 200:
        return 0
    else:
        return -1 


def get_given_light(headers):
    resp = requests.get("https://inzynierka-server.herokuapp.com/api/devices/" + str(BULB_ID) + "/", headers=headers)
    json = resp.json()
    if json["state"]:
        return json["state_value"]
    return 15


def get_authorization_key():
    login = {"email": "root@email.com", "password": "2wsxcde3"}
    resp = requests.post("https://inzynierka-server.herokuapp.com/api/auth/jwt/create/", json=login)
    headers = {"Authorization": "Bearer " + format(resp.json()["access"])}
    return headers


def main_loop(headers):
    status = write_light(headers, light_controller)
    if status == -1:
        print("There was an error while writing light")
    else:
        print("Successfully added light measurement")
    light_controller.control_light(get_given_light())
    time.sleep(60)


def write_light(headers):
    json = {"measure_value": round(readLight(), 3), "measuring_device": LIGHT_SENSOR_ID}
    resp = requests.post("https://inzynierka-server.herokuapp.com/api/daily-measurements/", json=json, headers=headers)
    if resp.status_code == 201:
        return 0
    else:
        print(resp.status_code)
        return -1


light_controller = LightController(BULB_IP)
time.sleep(5)

while True:
    print("hello")
    main_loop(get_authorization_key(), light_controller)

