import graphene
from graphene_django import DjangoObjectType

from ...core.types import BaseDecimal
from ...account.types import User
from ...channel.types import Channel
from ...order.types import Order
from ..models import Udhaar, SundayCollection


class UdhaarType(DjangoObjectType):
    id = graphene.ID(required=True)
    user = graphene.Field(User)
    shop = graphene.Field(Channel)
    order = graphene.Field(Order)
    amount = graphene.Field(BaseDecimal)
    paid_amount = graphene.Field(BaseDecimal)
    remaining = graphene.Field(BaseDecimal)
    due_date = graphene.DateTime()
    is_overdue = graphene.Boolean()
    status = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    
    class Meta:
        model = Udhaar
        fields = "__all__"


class SundayCollectionType(DjangoObjectType):
    id = graphene.ID(required=True)
    delivery_boy = graphene.Field(User)
    user = graphene.Field(User)
    udhaar = graphene.Field(UdhaarType)
    amount = graphene.Field(BaseDecimal)
    collected_amount = graphene.Field(BaseDecimal)
    status = graphene.String()
    collection_date = graphene.Date()
    collected_at = graphene.DateTime()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    
    class Meta:
        model = SundayCollection
        fields = "__all__"
