import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from models import CharactersModel


class CharactersFilter(FilterSet):
    class Meta:
        model = CharactersModel
        fields = {
            'name': [...],
            'cursed_technique': [...],
            'occupation': [...],
            'notes': [...],
        }

class CharactersTypeDef(SQLAlchemyObjectType):
    class Meta:
        model = CharactersModel
        interfaces = (relay.Node,)

## For mutations
class CharacterFields:
    id = graphene.Int()
    name = graphene.String()
    occupation = graphene.String()
    cursed_technique = graphene.String()
    img_file = graphene.String()
    notes = graphene.String()


class AddCharacterFields(graphene.InputObjectType, CharacterFields):
    pass
