import graphene
from graphene_django import DjangoObjectType

from ...account.types import User
from ...core.decorators import permission_required
from ...core.permissions import AccountPermissions
from ...order.types import Order
from ..models import DeliveryBoy, DeliveryAssignment, DeliveryLocation
from ..types import DeliveryBoyType, DeliveryAssignmentType, DeliveryLocationType


class DeliveryLocationUpdateInput(graphene.InputObjectType):
    latitude = graphene.Float(required=True)
    longitude = graphene.Float(required=True)
    speed = graphene.Float()
    battery_level = graphene.Int()


class DeliveryAssignmentAcceptInput(graphene.InputObjectType):
    assignment_id = graphene.ID(required=True)


class DeliveryAssignmentVerifyOTPInput(graphene.InputObjectType):
    assignment_id = graphene.ID(required=True)
    otp = graphene.String(required=True)


class DeliveryMutations(graphene.ObjectType):
    update_delivery_location = graphene.Field(
        DeliveryLocationType,
        description="Update delivery boy location",
        input=DeliveryLocationUpdateInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
    
    accept_delivery_assignment = graphene.Field(
        DeliveryAssignmentType,
        description="Accept delivery assignment",
        input=DeliveryAssignmentAcceptInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
    
    verify_delivery_otp = graphene.Field(
        DeliveryAssignmentType,
        description="Verify delivery OTP",
        input=DeliveryAssignmentVerifyOTPInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
