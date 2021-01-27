from bh1750 import readLight
import requests
import time
from light import LightController
from heater import HeaterController
from humidity import readTemperature, readHumidity
import threading

LIGHT_SENSOR_ID = 3
BULB_IP = "192.168.1.96"
HEATER_PIN = 6
BULB_ID = 2
HEATER_ID = 3
TERMOMETER_ID = 4
HYGROMETER_ID = 5
given_light = 150
given_temperature = 20
heater_state = False
bulb_state = False


def save_daily_average(headers):
    resp = requests.get("https://inzynierka-server.herokuapp.com/api/daily-measurements/1/reset/", headers=headers)
    if resp == 200:
        return 0
    else:
        return -1 


def get_given_light(headers):
    global bulb_state
    resp = requests.get("https://inzynierka-server.herokuapp.com/api/devices/" + str(BULB_ID) + "/", headers=headers)
    json = resp.json()
    if json["state"]:
        bulb_state = True
        return float(json["state_value"])
    bulb_state = False
    return 15


def get_given_temperature(headers):
    global heater_state
    resp = requests.get("https://inzynierka-server.herokuapp.com/api/devices/" + str(HEATER_ID) + "/", headers=headers)
    json = resp.json()
    if json["state"]:
        heater_state = True
        return float(json["state_value"])
    bulb_state = False
    return 18


def get_authorization_key():
    login = {"email": "root@email.com", "password": "2wsxcde3"}
    resp = requests.post("https://inzynierka-server.herokuapp.com/api/auth/jwt/create/", json=login)
    headers = {"Authorization": "Bearer " + format(resp.json()["access"])}
    return headers


def control_heater(heater):
    while True:
        print(given_temperature)
        if given_temperature > readTemperature() and heater_state:
            print("turning on heater")
            heater.turn_on()
        else:
            print("turning off heater")
            heater.turn_off()
        time.sleep(5)


def control_light(light):
    while True:
        if bulb_state:
            light.turnOn()
            light.setBrightness(given_light)
        else:
            light.turnOff()
        time.sleep(5)


def get_parameters(headers):
    global given_light, given_temperature
    while True:
        given_light = get_given_light(headers)
        given_temperature = get_given_temperature(headers)
        time.sleep(5)


def write_parameters(headers):
    while True:
        write_light(headers)
        write_temperature(headers)
        write_humidity(headers)
        time.sleep(120)


def write_light(headers):
    json = {"measure_value": round(readLight(), 3), "measuring_device": LIGHT_SENSOR_ID}
    resp = requests.post("https://inzynierka-server.herokuapp.com/api/daily-measurements/", json=json, headers=headers)
    return resp


def write_temperature(headers):
    json = {"measure_value": round(readTemperature(), 3), "measuring_device": TERMOMETER_ID}
    resp = requests.post("https://inzynierka-server.herokuapp.com/api/daily-measurements/", json=json, headers=headers)
    return resp


def write_humidity(headers):
    json = {"measure_value": round(readHumidity(), 3), "measuring_device": HYGROMETER_ID}
    resp = requests.post("https://inzynierka-server.herokuapp.com/api/daily-measurements/", json=json, headers=headers)
    return resp


headers = get_authorization_key()
data_saving_thread = threading.Thread(target=write_parameters, args=[headers])
data_reading_thread = threading.Thread(target=get_parameters, args=[headers])
heater_control_thread = threading.Thread(target=control_heater, args=[HeaterController(HEATER_PIN)])
light_control_thread = threading.Thread(target=control_light, args=[LightController(BULB_IP)])
heater_control_thread.start()
light_control_thread.start()
data_saving_thread.start()
data_reading_thread.start()
