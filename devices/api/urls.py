from django.urls import include, path
from rest_framework import routers

from devices.api.views import (
    BuildingViewSet,
    DeviceViewSet,
    MeasuringDeviceViewSet,
    MeasurementViewSet,
    RoomViewSet,
    SceneViewSet,
)

app_name = "devices"

router = routers.SimpleRouter()
router.register(r"devices", DeviceViewSet)
router.register(r"measuring-devices", MeasuringDeviceViewSet)
router.register(r"rooms", RoomViewSet)
router.register(r"scenes", SceneViewSet)
router.register(r"buildings", BuildingViewSet)
router.register(r"measurements", MeasurementViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
