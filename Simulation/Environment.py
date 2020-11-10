class Environment:
    def __init__(self, init_temperature, init_humidity, init_brightness):
        self.temperature = init_temperature
        self.humidity = init_humidity
        self.brightness = init_brightness
        self.heater_state = False
        self.blinds_state = False
        self.light_state = False
        self.air_conditioning_state = False
        self.max_temperature = 35  # depends on heater's power
        self.min_temperature = 15
        self.max_humidity = 70
        self.min_humidity = 20
        self.slow = 1000000

    def turn_on_heater(self):
        self.heater_state = True

    def turn_off_heater(self):
        self.heater_state = False

    def turn_on_air_conditioning(self):
        self.air_conditioning_state = True

    def turn_off_air_conditioning(self):
        self.air_conditioning_state = False

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def pass_time(self, delta_time):
        self.involve_heater(delta_time)
        self.involve_air_conditioning(delta_time)

    def involve_heater(self, delta_time):
        if self.heater_state:
            self.temperature += (self.max_temperature - self.temperature) * delta_time / self.slow
        else:
            self.temperature -= (self.temperature - self.min_temperature) * delta_time / self.slow
        self.limit_temperature()

    def involve_air_conditioning(self, delta_time):
        if self.air_conditioning_state:
            self.temperature -= (self.temperature - self.min_temperature) * delta_time / self.slow
            self.humidity -= self.humidity * delta_time / self.slow
        else:
            self.humidity += self.humidity * delta_time / self.slow
        self.limit_temperature()
        self.limit_humidity()

    def limit_temperature(self):
        if self.temperature > self.max_temperature:
            self.temperature = self.max_temperature
        if self.temperature < self.min_temperature:
            self.temperature = self.min_temperature

    def limit_humidity(self):
        if self.humidity > self.max_humidity:
            self.humidity = self.max_humidity
        if self.humidity < self.min_humidity:
            self.humidity = self.min_humidity
