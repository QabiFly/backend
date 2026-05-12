import graphene
from graphene_django import DjangoObjectType

from ...account.types import User
from ...core.types import BaseDecimal
from ..models import Udhaar, SundayCollection
from ..types import UdhaarType, SundayCollectionType


class KhataQueries(graphene.ObjectType):
    my_udhaar = graphene.List(
        UdhaarType,
        description="Get all Udhaar records for authenticated user",
        resolver=lambda self, info: Udhaar.objects.filter(user=info.context.user)
    )
    
    my_sunday_collections = graphene.List(
        SundayCollectionType,
        description="Get all Sunday collections for delivery boy",
        resolver=lambda self, info: SundayCollection.objects.filter(delivery_boy=info.context.user)
    )
