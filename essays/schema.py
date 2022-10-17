import graphene

# from django.db import models
# from graphene.types import schema
from graphene_django import DjangoObjectType  # , DjangoListField

from .models import Essay


class EssayType(DjangoObjectType):
    class Meta:
        model = Essay
        fields = ("id",)


class Query(graphene.ObjectType):

    all_essays = graphene.List(EssayType)  # DjangoListField(EssayType)

    def resolve_all_essays(root, info, **kwargs):
        return Essay.objects.all()


schema = graphene.Schema(query=Query)
