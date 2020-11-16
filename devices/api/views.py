from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from devices.models import Building, Device, MeasuringDevice, Measurement, Room, Scene
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
        return self.queryset.filter(building__user == self.request.user)


class MeasuringDeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeasuringDevice.objects.all()
    serializer_class = MeasuringDeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(building__user=self.request.user)

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
        return self.queryset.filter(building__user=self.request.user)


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
        return Sself.queryset.filter(building__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return self.serializer_class