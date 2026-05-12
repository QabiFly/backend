import graphene
from graphene_django import DjangoObjectType

from ...account.types import User
from ...core.decorators import permission_required
from ...core.permissions import AccountPermissions
from ...core.types import BaseDecimal
from ..models import Wallet, WalletTransaction
from ..types import WalletType, WalletTransactionType


class WalletTopupInput(graphene.InputObjectType):
    amount = graphene.Decimal(required=True)
    method = graphene.String(required=True)


class WalletWithdrawInput(graphene.InputObjectType):
    amount = graphene.Decimal(required=True)
    upi_id = graphene.String(required=True)


class WalletTransferInput(graphene.InputObjectType):
    to_user_id = graphene.ID(required=True)
    amount = graphene.Decimal(required=True)


class WalletMutations(graphene.ObjectType):
    topup_wallet = graphene.Field(
        WalletType,
        description="Top-up wallet",
        input=WalletTopupInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
    
    withdraw_wallet = graphene.Field(
        WalletType,
        description="Withdraw from wallet",
        input=WalletWithdrawInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
    
    transfer_wallet = graphene.Field(
        WalletType,
        description="Transfer to another user",
        input=WalletTransferInput(),
        permission_classes=[permission_required(AccountPermissions.MANAGE_ORDERS)]
    )
