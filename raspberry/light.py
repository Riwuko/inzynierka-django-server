import time
from bh1750 import readLight
from yeelight import Bulb


class LightController:
    def __init__(self, bulb_ip):
        self.bulb = Bulb(bulb_ip)
        self.bulb_power = 0
        self.bulb.set_brightness(self.bulb_power)

    def turnOn(self):
        self.bulb.turn_on()

    def turnOff(self):
        self.bulb.turn_off()

    def setBrightness(self, brightness):
        self.bulb.set_brightness(brightness)

    def control_light(self, given_intensity):
        print(readLight())
        print(given_intensity)
        if readLight() > given_intensity:
            self.decrease_bulb_power(given_intensity)
        else:
            self.increase_bulb_power(given_intensity)
        return self.bulb_power

    def increase_bulb_power(self, given_intensity):
        while readLight() < given_intensity:
            self.bulb_power += 1
            if self.bulb_power > 100:
                self.bulb_power = 100
                break
            self.bulb.set_brightness(self.bulb_power)
            time.sleep(1)

    def decrease_bulb_power(self, given_intensity):
        while readLight() > given_intensity:       
            self.bulb_power -= 1
            if self.bulb_power < 0:
                 self.bulb_power = 0
                 break
            self.bulb.set_brightness(self.bulb_power)
            time.sleep(1)
