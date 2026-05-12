import graphene
from graphene_django import DjangoObjectType

from ...account.types import User
from ...core.decorators import permission_required
from ...core.permissions import AccountPermissions
from ...core.types import BaseDecimal
from ...order.types import Order
from ...channel.types import Channel
from ..models import Udhaar, SundayCollection
from ..types import UdhaarType, SundayCollectionType


class UdhaarCreateInput(graphene.InputObjectType):
    user_id = graphene.ID(required=True)
    shop_id = graphene.ID(required=True)
    order_id = graphene.ID()
    amount = graphene.Decimal(required=True)
    due_date = graphene.DateTime()


class UdhaarPayInput(graphene.InputObjectType):
    udhaar_id = graphene.ID(required=True)
    amount = graphene.Decimal(required=True)


class SundayCollectionCreateInput(graphene.InputObjectType):
    delivery_boy_id = graphene.ID(required=True)
    user_id = graphene.ID(required=True)
    udhaar_id = graphene.ID(required=True)
    amount = graphene.Decimal(required=True)
    collection_date = graphene.Date(required=True)


class SundayCollectionCollectInput(graphene.InputObjectType):
    collection_id = graphene.ID(required=True)
    amount = graphene.Decimal(required=True)


class KhataMutations(graphene.ObjectType):
    create_udhaar = graphene.Field(
        UdhaarType,
        description="Create new Udhaar record",
        input=UdhaarCreateInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
    
    pay_udhaar = graphene.Field(
        UdhaarType,
        description="Pay Udhaar amount",
        input=UdhaarPayInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
    
    create_sunday_collection = graphene.Field(
        SundayCollectionType,
        description="Create new Sunday collection",
        input=SundayCollectionCreateInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
    
    collect_sunday_collection = graphene.Field(
        SundayCollectionType,
        description="Collect Sunday collection amount",
        input=SundayCollectionCollectInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
