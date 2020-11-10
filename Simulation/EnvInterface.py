from Environment import Environment
import time


class IEnvironment:
    def __init__(self, init_temperature=20, init_humidity=45, init_brightness=10):
        self.environment = Environment(init_temperature, init_humidity, init_brightness)

    def run_simulation(self):
        simulation_should_end = False
        while not simulation_should_end:
            self.environment.pass_time(100)
            time.sleep(0.1)

    def get_temperature(self):
        return self.environment.get_temperature()

    def get_humidity(self):
        return self.environment.get_humidity()

    def turn_on_heater(self):
        self.environment.turn_on_heater()

    def turn_off_heater(self):
        self.environment.turn_off_heater()

    def turn_on_air_conditioning(self):
        self.environment.turn_on_air_conditioning()

    def turn_off_air_conditioning(self):
        self.environment.turn_off_air_conditioning()