"""
QabiFly GraphQL Schema
Extended Saleor GraphQL schema with QabiFly-specific mutations and queries
"""

import graphene
from graphene_django import DjangoObjectType

# Import QabiFly app mutations
from ..khata.graphql.mutations import KhataMutations
from ..wallet.graphql.mutations import WalletMutations
from ..delivery.graphql.mutations import DeliveryMutations

# Import QabiFly app queries
from ..khata.graphql.queries import KhataQueries
from ..wallet.graphql.queries import WalletQueries
from ..delivery.graphql.queries import DeliveryQueries


class Query(KhataQueries, WalletQueries, DeliveryQueries, graphene.ObjectType):
    """QabiFly Root Query"""
    pass


class Mutation(KhataMutations, WalletMutations, DeliveryMutations, graphene.ObjectType):
    """QabiFly Root Mutation"""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
