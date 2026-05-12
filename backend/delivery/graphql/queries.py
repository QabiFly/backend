import graphene
from graphene_django import DjangoObjectType

from ...account.types import User
from ...core.types import BaseDecimal
from ..models import DeliveryBoy, DeliveryAssignment, DeliveryLocation
from ..types import DeliveryBoyType, DeliveryAssignmentType, DeliveryLocationType


class DeliveryQueries(graphene.ObjectType):
    live_deliveries = graphene.List(
        DeliveryLocationType,
        description="Get live delivery locations",
        resolver=lambda self, info: DeliveryLocation.objects.order_by('-recorded_at')[:10]
    )
