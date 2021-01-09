from devices.models import Building, ControlParameter, DailyMeasurement, Device, MeasuringDevice, Measurement, Room, Scene, SceneDeviceState
from rest_framework import serializers


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class DeviceStateUpdateSerializer(serializers.Serializer):
    state = serializers.BooleanField()

class ControlParameterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ControlParameter
        fields = "__all__"

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"

class DailyMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMeasurement
        fields = "__all__"

class MeasuringDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuringDevice
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


class SceneDeviceStateSerializer(serializers.Serializer):
    device_id = serializers.IntegerField()
    state = serializers.BooleanField()


class SceneSerializer(serializers.ModelSerializer):
    scene_devices_states = SceneDeviceStateSerializer(many=True, read_only=True)

    class Meta:
        model = Scene
        fields = "__all__"
        extra_fields = ["scene_devices_states"]


class SceneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = "__all__"


class ScenePostSerializer(serializers.Serializer):
    scene = SceneSerializer
    devices = SceneDeviceStateSerializer(many=True)


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


class IsActiveSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
