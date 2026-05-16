"""
Saleor GraphQL Schema
Extended Saleor GraphQL schema with Saleor-specific mutations and queries
"""

import graphene
from graphene_django import DjangoObjectType

# Import Saleor app mutations
from ..khata.graphql.mutations import KhataMutations
from ..wallet.graphql.mutations import WalletMutations
from ..delivery.graphql.mutations import DeliveryMutations

# Import Saleor app queries
from ..khata.graphql.queries import KhataQueries
from ..wallet.graphql.queries import WalletQueries
from ..delivery.graphql.queries import DeliveryQueries


class Query(KhataQueries, WalletQueries, DeliveryQueries, graphene.ObjectType):
    """Saleor Root Query"""
    pass


class Mutation(KhataMutations, WalletMutations, DeliveryMutations, graphene.ObjectType):
    """Saleor Root Mutation"""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
