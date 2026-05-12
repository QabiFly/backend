import graphene
from graphene_django import DjangoObjectType

from ...account.types import User
from ...core.types import BaseDecimal
from ..models import Wallet, WalletTransaction
from ..types import WalletType, WalletTransactionType


class WalletQueries(graphene.ObjectType):
    my_wallet = graphene.Field(
        WalletType,
        description="Get wallet details for authenticated user",
        resolver=lambda self, info: Wallet.objects.get_or_create(user=info.context.user)
    )
    
    my_transactions = graphene.List(
        WalletTransactionType,
        description="Get wallet transactions for authenticated user",
        resolver=lambda self, info: WalletTransaction.objects.filter(wallet__user=info.context.user)
    )
