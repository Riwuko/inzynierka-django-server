import Adafruit_DHT as dht

DHT_PIN = 4


def readTemperature():
    h, t = dht.read_retry(dht.DHT22, DHT_PIN)
    return t


def readHumidity():
    h, t = dht.read_retry(dht.DHT22, DHT_PIN)
    return h
