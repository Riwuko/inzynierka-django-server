from django.urls import include, path
from rest_framework import routers

from devices.api.views import (
    BuildingViewSet,
    DeviceViewSet,
    DailyMeasurementViewSet,
    MeasuringDeviceViewSet,
    MeasuringDeviceMeasurements,
    MeasuringDeviceDailyMeasurements,
    MeasurementViewSet,
    RoomViewSet,
    SceneViewSet,
)

app_name = "devices"

router = routers.SimpleRouter()
router.register(r"devices", DeviceViewSet)
router.register(r"measuring-devices", MeasuringDeviceViewSet)
router.register(r"rooms", RoomViewSet)
router.register(r"buildings", BuildingViewSet)
router.register(r"measurements", MeasurementViewSet)
router.register(r"scenes", SceneViewSet)
router.register(r"daily-measurements", DailyMeasurementViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "measuring-devices/<int:pk>/measurements/",
        MeasuringDeviceMeasurements.as_view(),
        name="measuring-devices-measurements",
    ),
    path(
        "measuring-devices/<int:pk>/daily-measurements/",
        MeasuringDeviceDailyMeasurements.as_view(),
        name="measuring-devices-daily-measurements",
    ),
]
