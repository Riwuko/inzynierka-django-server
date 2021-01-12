from __future__ import absolute_import

import datetime
from statistics import mean
from collections import defaultdict
from django.db.models import Q, Avg
from server_config.celery import app
from devices.models import Measurement, DailyMeasurement, MeasuringDevice
from pprint import pprint


@app.task
def check_temperature():
    print("Hello there!")


@app.task
def move_daily_measurement_to_measurement():
    if not DailyMeasurement.objects.all():
        return
    hours_ranges = [(6, 12, 9), (12, 18, 15), (18, 24, 21), (24, 6, 3)]  # start, end, middle
    measurements = []
    for device in MeasuringDevice.objects.all():
        for hours in hours_ranges:
            timeday_measure_values = [
                measurement.measure_value
                for measurement in DailyMeasurement.objects.filter(
                    Q(measure_date__hour__range=hours[0:2])
                    & Q(measuring_device=device)
                )
            ]
            date = DailyMeasurement.objects.first()
            measurements.append(
                {
                    "measuring_device": device,
                    "measure_date": date.measure_date.replace(hour=hours[2], minute=00, second=00),
                    "measure_value": mean(timeday_measure_values)
                    if timeday_measure_values
                    else None,
                }
            )
    Measurement.objects.bulk_create([Measurement(**measurement) for measurement in measurements])
    DailyMeasurement.objects.all().delete()
