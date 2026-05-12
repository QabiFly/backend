import graphene
from graphene_django import DjangoObjectType

from ...core.types import BaseDecimal
from ...account.types import User
from ..models import Wallet, WalletTransaction


class WalletType(DjangoObjectType):
    id = graphene.ID(required=True)
    user = graphene.Field(User)
    balance = graphene.Field(BaseDecimal)
    pending_balance = graphene.Field(BaseDecimal)
    available_balance = graphene.Field(BaseDecimal)
    total_earned = graphene.Field(BaseDecimal)
    total_withdrawn = graphene.Field(BaseDecimal)
    upi_id = graphene.String()
    is_active = graphene.Boolean()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    
    class Meta:
        model = Wallet
        fields = "__all__"


class WalletTransactionType(DjangoObjectType):
    id = graphene.ID(required=True)
    wallet = graphene.Field(WalletType)
    amount = graphene.Field(BaseDecimal)
    transaction_type = graphene.String()
    purpose = graphene.String()
    order = graphene.Field('order.Order')
    balance_after = graphene.Field(BaseDecimal)
    description = graphene.String()
    status = graphene.String()
    created_at = graphene.DateTime()
    
    class Meta:
        model = WalletTransaction
        fields = "__all__"
