import graphene

from accounts.schema import Query as accountsQuery


class Query(accountsQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
