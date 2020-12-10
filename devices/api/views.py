import json
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from devices.models import Building, Device, MeasuringDevice, Measurement, Room, Scene, SceneDeviceState
from devices.api.serializers import (
    BuildingSerializer,
    BuildingListSerializer,
    DeviceSerializer,
    MeasurementSerializer,
    MeasuringDeviceSerializer,
    RoomSerializer,
    RoomListSerializer,
    SceneSerializer,
    SceneListSerializer,
    SceneDeviceStateSerializer,
    SceneDeviceStatePostSerializer,
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


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(room__building__user=self.request.user)


class MeasuringDeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeasuringDevice.objects.all()
    serializer_class = MeasuringDeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(room__building__user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        measuring_device = self.get_object()
        try:
            measurement = Measurement.objects.last()
            response_data = {
                **self.serializer_class(measuring_device).data,
                **MeasurementSerializer(measurement).data,
            }

        except Measurement.DoesNotExist:
            response_data = self.serializer_class(measuring_device).data

        return Response(response_data, status=status.HTTP_200_OK)


class MeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

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


class SceneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    list_serializer_class = SceneListSerializer

    def get_queryset(self):
        return self.queryset.filter(building__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return self.serializer_class


class SceneDevicesView(generics.ListCreateAPIView):
    queryset = SceneDeviceState.objects.all()
    serializer_class = SceneDeviceStateSerializer

    def get_queryset(self):
        return self.queryset.filter(scene__pk=self.kwargs["pk"], scene__building__user=self.request.user)

    def post(self, request, *args, **kwargs):
        scene = get_object_or_404(Scene, id=self.kwargs.get("pk"))
        serializer = SceneDeviceStatePostSerializer(data=request.data.get("devices"), many=True)

        if serializer.is_valid(raise_exception=True):
            for device in serializer.data:
                device["scene"] = scene
                device["device"] = get_object_or_404(Device, id=device["device_id"])

            SceneDeviceState.objects.bulk_create(
                [SceneDeviceState(**device) for device in serializer.data], ignore_conflicts=True
            )
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
