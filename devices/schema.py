import graphene
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from devices.models import Building, Device, Measurement, MeasuringDevice, Room, Scene


class BuildingType(DjangoObjectType):
    class Meta:
        model = Building


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device


class MeasurementType(DjangoObjectType):
    class Meta:
        model = Measurement


class MeasuringDeviceType(DjangoObjectType):
    class Meta:
        model = MeasuringDevice


class RoomType(DjangoObjectType):
    class Meta:
        model = Room


class SceneType(DjangoObjectType):
    class Meta:
        model = Scene


class Query(graphene.ObjectType):
    buildings = graphene.List(BuildingType)
    building = graphene.Field(BuildingType, id=graphene.Int())

    devices = graphene.List(DeviceType)
    device = graphene.Field(DeviceType, id=graphene.Int())

    measurements = graphene.List(MeasurementType)
    measurement = graphene.Field(MeasurementType, id=graphene.Int())

    measuring_devices = graphene.List(MeasuringDeviceType)
    measuring_device = graphene.Field(MeasuringDeviceType, id=graphene.Int())

    rooms = graphene.List(RoomType)
    room = graphene.Field(RoomType, id=graphene.Int())

    scenes = graphene.List(SceneType)
    scene = graphene.Field(SceneType, id=graphene.Int())

    @login_required
    def resolve_buildings(root, info):
        return Building.objects.filter(user=info.context.user)

    @login_required
    def resolve_building(root, info, id):
        building = get_object_or_404(Building, id=id)
        return building

    @login_required
    def resolve_devices(root, info):
        return Device.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_device(root, info, id):
        device = get_object_or_404(Device, id=id, building__user=info.context.user)
        return device

    @login_required
    def resolve_measuring_devices(root, info):
        return MeasuringDevice.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_measuring_device(root, info, id):
        device = get_object_or_404(MeasuringDevice, id=id, building__user=info.context.user)
        return device

    @login_required
    def resolve_measurements(root, info):
        return Measurement.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_measurement(root, info, id):
        measurement = get_object_or_404(Device, id=id, building__user=info.context.user)
        return measurement

    @login_required
    def resolve_rooms(root, info):
        return Room.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_room(root, info, id):
        room = get_object_or_404(Device, id=id, building__user=info.context.user)
        return room

    @login_required
    def resolve_scenes(root, info):
        return Scene.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_scene(root, info, id):
        scene = get_object_or_404(Device, id=id, building__user=info.context.user)
        return scenes


class ChangeDeviceState(graphene.Mutation):
    device = graphene.Field(DeviceType)

    class Arguments:
        state = graphene.Boolean()

    @login_required
    def mutate(root, info, id, **kwargs):
        device = get_object_or_404(Device, id=id, building__user=info.context.user)
        device.state = kwargs.get("state", device.state)
        device.save()
        return ChangeDeviceState


class Mutation(graphene.ObjectType):
    update_device = ChangeDeviceState()
