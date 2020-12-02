import graphene
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from devices.models import Building, Device, Measurement, MeasuringDevice, Room, Scene
from users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


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
    buildings = graphene.List(BuildingType, token=graphene.String(required=True))
    building = graphene.Field(BuildingType, id=graphene.Int(), token=graphene.String(required=True))

    devices = graphene.List(DeviceType, token=graphene.String(required=True))
    device = graphene.Field(DeviceType, id=graphene.Int(), token=graphene.String(required=True))

    measurements = graphene.List(MeasurementType, token=graphene.String(required=True))
    measurement = graphene.Field(MeasurementType, id=graphene.Int(), token=graphene.String(required=True))

    measuring_devices = graphene.List(MeasuringDeviceType,  token=graphene.String(required=True))
    measuring_device = graphene.Field(MeasuringDeviceType, id=graphene.Int(),  token=graphene.String(required=True))

    rooms = graphene.List(RoomType,  token=graphene.String(required=True))
    room = graphene.Field(RoomType, id=graphene.Int(),  token=graphene.String(required=True))

    scenes = graphene.List(SceneType, token=graphene.String(required=True),  token=graphene.String(required=True))
    scene = graphene.Field(SceneType, id=graphene.Int(),  token=graphene.String(required=True))

    users = graphene.List(UserType, token=graphene.String(required=True))
    user = graphene.Field(UserType, id=graphene.Int(), token=graphene.String(required=True))

    @login_required
    def resolve_buildings(root, info,**kwargs):
        return Building.objects.filter(user=info.context.user)

    @login_required
    def resolve_building(root, info, id, **kwargs):
        return get_object_or_404(Building, id=id)

    @login_required
    def resolve_devices(root, info, **kwargs):
        return Device.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_device(root, info, id, **kwargs):
        return get_object_or_404(Device, id=id, building__user=info.context.user)

    @login_required
    def resolve_measuring_devices(root, info, **kwargs):
        return MeasuringDevice.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_measuring_device(root, info, id, **kwargs):
        return get_object_or_404(MeasuringDevice, id=id, building__user=info.context.user)

    @login_required
    def resolve_measurements(root, info, **kwargs):
        return Measurement.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_measurement(root, info, id, **kwargs):
        return get_object_or_404(Measurement, id=id, building__user=info.context.user)

    @login_required
    def resolve_rooms(root, info, **kwargs):
        return Room.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_room(root, info, id, **kwargs):
        return get_object_or_404(Room, id=id, building__user=info.context.user)

    @login_required
    def resolve_scenes(root, info, **kwargs):
        return Scene.objects.filter(building__user=info.context.user)

    @login_required
    def resolve_scene(root, info, id, **kwargs):
        return get_object_or_404(Scene, id=id, building__user=info.context.user)

    @login_required
    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    @login_required
    def resolve_user(root, info, id, **kwargs):
        return get_object_or_404(User, id=id)


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
