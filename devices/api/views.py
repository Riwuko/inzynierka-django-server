import distutils
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import mixins, views
from datetime import datetime, time

from devices.tasks import move_daily_measurement_to_measurement

from devices.models import (
    Building,
    ControlParameter,
    DailyMeasurement,
    Device,
    MeasuringDevice,
    Measurement,
    Room,
    Scene,
    SceneDeviceState,
)
from devices.api.serializers import (
    BuildingSerializer,
    BuildingListSerializer,
    ControlParameterSerializer,
    DailyMeasurementSerializer,
    DeviceSerializer,
    DeviceStateUpdateSerializer,
    IsActiveSerializer,
    MeasurementSerializer,
    MeasuringDeviceSerializer,
    RoomSerializer,
    RoomListSerializer,
    SceneSerializer,
    SceneListSerializer,
    ScenePostSerializer,
    SceneDeviceStateSerializer,
)


class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    list_serializer_class = BuildingListSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class DeviceViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(room__building__user=self.request.user)

    def patch(self, request, *args, **kwargs):
        device = self.get_object()
        serializer = DeviceStateUpdateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            device.state = serializer.data.get("state", False)
            device.state_value = serializer.data.get("state_value", None)
            device.save()
            device_serializer = self.get_serializer(device)
            return Response(data=device_serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class MeasuringDeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeasuringDevice.objects.all()
    serializer_class = MeasuringDeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(room__building__user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        measuring_device = self.get_object()
        try:
            measurement = DailyMeasurement.objects.filter(measuring_device=measuring_device).last()
            response_data = {
                **self.serializer_class(measuring_device).data,
                "last_measure_date": MeasurementSerializer(measurement).data.get("measure_date"),
                "last_measure_value": MeasurementSerializer(measurement).data.get("measure_value"),
            }

        except Measurement.DoesNotExist:
            response_data = self.serializer_class(measuring_device).data

        return Response(response_data, status=status.HTTP_200_OK)


class MeasuringDeviceMeasurements(generics.ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        return self.queryset.filter(measuring_device__pk=self.kwargs["pk"])


class MeasuringDeviceDailyMeasurements(generics.ListAPIView):
    queryset = DailyMeasurement.objects.all()
    serializer_class = DailyMeasurementSerializer

    def get_queryset(self):
        return self.queryset.filter(measuring_device__pk=self.kwargs["pk"])


class MeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        return self.queryset.filter(measuring_device__room__building__user=self.request.user)


class DailyMeasurementViewSet(viewsets.ModelViewSet):
    queryset = DailyMeasurement.objects.all()
    serializer_class = DailyMeasurementSerializer

    def get_queryset(self):
        return self.queryset.filter(measuring_device__room__building__user=self.request.user)


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    list_serializer_class = RoomListSerializer

    def get_queryset(self):
        return self.queryset.filter(building__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return self.serializer_class


class SceneViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    list_serializer_class = SceneListSerializer
    post_serializer_class = ScenePostSerializer

    def get_queryset(self):
        return self.queryset.filter(building__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action == "create":
            return self.post_serializer_class
        return self.serializer_class

    def _get_devices_for_update(self, scene):
        configurations = SceneDeviceState.objects.filter(scene__id=scene.id)
        for configuration in configurations:
            configuration.device.state = configuration.state
            configuration.device.state_value = configuration.state_value
        return [device.device for device in configurations]

    def update(self, request, *args, **kwargs):
        """Custom patch method - takes scene id and changes devices states"""
        scene = self.get_object()
        if scene is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        is_active_serializer = IsActiveSerializer(data=request.data)
        if not is_active_serializer.is_valid(raise_exception=True):
            return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)

        scene.is_active = is_active_serializer.data.get("is_active", False)
        scene.save()
        scene_serializer = self.serializer_class(scene)

        if not scene.is_active:
            return Response(data=scene_serializer.data, status=status.HTTP_200_OK)

        devices = self._get_devices_for_update(scene)
        Device.objects.bulk_update(devices, fields=("state","state_value",))

        return Response(data=scene_serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Custom post method - takes scene id and devices ids and states for creating new Scene object and SceneDeviceState object"""
        scene_serializer = self.serializer_class(data=request.data.get("scene"))
        if not scene_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        scene = scene_serializer.save()
        devices = request.data.get("devices")

        id_list = [device["device_id"] for device in devices]
        device_objects = Device.objects.filter(id__in=id_list)
        scene_device_states = [
            {
                "device": device_objects.get(id=device["device_id"]),
                "state": device.get("state", False),
                "state_value": device.get("state_value", None),
                "scene": scene,
            }
            for device in devices
        ]

        SceneDeviceState.objects.bulk_create(
            [SceneDeviceState(**device) for device in scene_device_states],
            ignore_conflicts=True,
        )

        return Response(data=scene_serializer.data, status=status.HTTP_200_OK)

class ControlParameterViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ControlParameter.objects.all()
    serializer_class = ControlParameterSerializer


class RoomControlParameter(generics.ListAPIView):
    queryset = ControlParameter.objects.all()
    serializer_class = ControlParameterSerializer

    def get_queryset(self):
        return self.queryset.filter(room__pk=self.kwargs["pk"])

@api_view(('GET',))
@staff_member_required
def reset_daily_measurements(request, **kwargs):
    # if not time(23, 00) <= datetime.now().time() >= time(23, 59):
    #     return Response(status=status.HTTP_403_FORBIDDEN)
    move_daily_measurement_to_measurement()
    return Response(status=status.HTTP_200_OK)
