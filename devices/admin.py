from django.contrib import admin

from devices.models import Building, Device, Measurement, MeasuringDevice, Room, Scene, SceneDeviceState

admin.site.register(Device)
admin.site.register(Measurement)
admin.site.register(MeasuringDevice)
admin.site.register(Room)
admin.site.register(Scene)
admin.site.register(Building)
admin.site.register(SceneDeviceState)
