from typedefs import CharactersTypeDef, CharactersFilter, AddCharacterFields
from models import CharactersModel
from database import db
import graphene
from graphene import relay
from graphene_sqlalchemy_filter import FilterableConnectionField


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    get_characters = FilterableConnectionField(CharactersTypeDef.connection, filters=CharactersFilter())

class AddNewCharacter(graphene.Mutation):
    character = graphene.Field(lambda: CharactersTypeDef)
    status = graphene.Boolean()

    class Arguments:
        input = AddCharacterFields(required=True)

    @staticmethod
    def mutate(self, info, input):
        character = CharactersModel(**input)
        # db.session.add(character)
        # db.session.commit()
        status = True
        return AddNewCharacter(character=character, status=status)


class Mutation(graphene.ObjectType):
    addNewCharacter = AddNewCharacter.Field()

schema = graphene.Schema(
    query=Query, mutation=Mutation
)
