from django.db import models

from users.models import User


class Building(models.Model):
    name = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, related_name="user_buildings", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Building: {str(self.id)} | name: {self.name}"


class Room(models.Model):
    name = models.CharField(max_length=100, null=False)
    building = models.ForeignKey(
        Building, related_name="building_rooms", null=False, on_delete=models.CASCADE
    )
    icon = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"Room: {str(self.id)} | name: {self.name}"


class MeasuringDevice(models.Model):
    name = models.CharField(max_length=100, null=False)
    room = models.ForeignKey(
        Room, related_name="room_measuring_devices", null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Measuring device: {str(self.id)} | name: {self.name}"


class Device(models.Model):
    name = models.CharField(max_length=100, null=False)
    state = models.BooleanField(null=False, default=False)
    measuring_device = models.ForeignKey(
        MeasuringDevice,
        related_name="measuring_device_devices",
        null=True,
        on_delete=models.SET_NULL,
    )
    room = models.ForeignKey(Room, related_name="room_devices", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Device: {str(self.id)} | name: {self.name}"


class Scene(models.Model):
    name = models.CharField(max_length=100, null=False)
    building = models.ForeignKey(
        Building, related_name="building_scenes", null=False, on_delete=models.CASCADE
    )
    icon = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"Scene: {str(self.id)} | name: {self.name}"


class SceneDeviceState(models.Model):
    device = models.ForeignKey(
        Device, related_name="device_scenes_states", null=False, on_delete=models.CASCADE
    )
    state = models.BooleanField(null=False, default=False)
    scene = models.ForeignKey(
        Scene, related_name="scene_devices_states", null=False, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            "device",
            "scene",
        )

    def __str__(self):
        return f"Scene-Device: {self.scene} -- {self.device}"


class Measurement(models.Model):
    measure_date = models.DateField(auto_now=True, null=False)
    measure_value = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    measuring_device = models.OneToOneField(MeasuringDevice, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Measurement: {str(self.id)} | measuring device: {self.measuring_device.name} | date: {self.measure_date}"
