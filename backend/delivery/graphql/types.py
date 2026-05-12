import graphene
from graphene_django import DjangoObjectType

from ...core.types import BaseDecimal
from ...account.types import User
from ...order.types import Order
from ..models import DeliveryBoy, DeliveryAssignment, DeliveryLocation


class DeliveryBoyType(DjangoObjectType):
    id = graphene.ID(required=True)
    user = graphene.Field(User)
    is_available = graphene.Boolean()
    is_online = graphene.Boolean()
    current_latitude = graphene.Float()
    current_longitude = graphene.Float()
    total_deliveries = graphene.Int()
    rating = graphene.Float()
    zone = graphene.String()
    vehicle_type = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    
    class Meta:
        model = DeliveryBoy
        fields = "__all__"


class DeliveryAssignmentType(DjangoObjectType):
    id = graphene.ID(required=True)
    order = graphene.Field(Order)
    delivery_boy = graphene.Field(User)
    status = graphene.String()
    delivery_otp = graphene.String()
    otp_verified = graphene.Boolean()
    assigned_at = graphene.DateTime()
    accepted_at = graphene.DateTime()
    delivered_at = graphene.DateTime()
    
    class Meta:
        model = DeliveryAssignment
        fields = "__all__"


class DeliveryLocationType(DjangoObjectType):
    id = graphene.ID(required=True)
    delivery_boy = graphene.Field(User)
    order = graphene.Field(Order)
    latitude = graphene.Float()
    longitude = graphene.Float()
    speed = graphene.Float()
    battery_level = graphene.Int()
    recorded_at = graphene.DateTime()
    
    class Meta:
        model = DeliveryLocation
        fields = "__all__"
