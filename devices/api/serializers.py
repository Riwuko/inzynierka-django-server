from devices.models import Building, Device, MeasuringDevice, Measurement, Room, Scene
from rest_framework import serializers


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class MeasuringDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuringDevice
        fields = "__all__"


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    room_devices = DeviceSerializer(many=True, read_only=True)
    room_measuring_devices = MeasuringDeviceSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        extra_fields = ["room_devices", "room_measuring_devices"]


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class SceneSerializer(serializers.ModelSerializer):
    scene_devices = DeviceSerializer(many=True, read_only=True)

    class Meta:
        model = Scene
        fields = "__all__"
        extra_fields = ["scene_devices"]


class SceneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = "__all__"


class BuildingSerializer(serializers.ModelSerializer):
    building_rooms = RoomListSerializer(many=True, read_only=True)
    building_scenes = SceneListSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = "__all__"
        extra_fields = ["building_rooms", "building_scenes"]


class BuildingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"