from dataclasses import dataclass, field
from enum import Enum
from typing import Any, NewType

from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses_jsonschema.field_types import FieldEncoder

ObjectType = NewType("ObjectType", int)


class ObjectTypeField(FieldEncoder[int, int]):
    @property
    def json_schema(self) -> dict[str, str]:
        return {"type_": "object"}


JsonSchemaMixin.register_field_encoders({ObjectType: ObjectTypeField()})


class Activity(Enum):
    IDLE = "IDLE"
    WALKING = "WALKING"
    ATTACKING = "ATTACKING"
    DEATH = "DEATH"


class Direction(Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


@dataclass
class Tile(JsonSchemaMixin):
    activity: Activity = Activity.IDLE
    direction: Direction = Direction.NORTH


@dataclass
class NPC(JsonSchemaMixin):
    interact_distance: int = 0
    interactable: bool = False


@dataclass
class Enemy(JsonSchemaMixin):
    speed: float = 0.0
    health: int = 100
    max_health: int = 100


@dataclass
class PatrolEnemy(Enemy, JsonSchemaMixin):
    patrol_path: ObjectType = ObjectType(-1)


class CustomInteraction(Enum):
    NONE = "NONE"
    TALKY = "TALKY"
    SHOP = "SHOP"
    RACE_START = "RACE_START"
    SCOREBOARD = "SCOREBOARD"
    RACE_STOP = "RACE_STOP"
    GIVE_ITEM = "GIVE_ITEM"
    DIG = "DIG"
    REQUIRE_ITEMS = "REQUIRE_ITEMS"
    RUNNER = "RUNNER"
    CUT_OUT = "CUT_OUT"
    LICENSE = "LICENSE"


@dataclass
class Interaction(JsonSchemaMixin):
    custom_attribute: str = ""
    custom_interaction: CustomInteraction = CustomInteraction.NONE
    loop: bool = False
    next_interaction: int = -1
    path: ObjectType = ObjectType(-1)
    speed: float = 0.0
    text: str = ""


class InteractionOn(Enum):
    NONE = "NONE"
    INTERACT = "INTERACT"
    COLLIDE = "COLLIDE"


@dataclass
class AreaObject(JsonSchemaMixin):
    area: ObjectType = ObjectType(-1)
    interaction_on: InteractionOn = InteractionOn.NONE
    interaction: Interaction = field(default_factory=lambda: Interaction())


@dataclass
class Pickupable(JsonSchemaMixin):
    description: str = ""
    quantity: int = 1
    icon: int = -1


class CustomLayerType(Enum):
    NONE = "NONE"
    DYNAMIC = "DYNAMIC"


@dataclass
class Layer(JsonSchemaMixin):
    type: CustomLayerType = CustomLayerType.NONE


class MazeTileType(Enum):
    NONE = "NONE"
    START_END = "START_END"
    CORNER_NE = "CORNER_NE"
    CORNER_SE = "CORNER_SE"
    CORNER_SW = "CORNER_SW"
    CORNER_NW = "CORNER_NW"
    MISSING = "MISSING"


@dataclass
class Maze(JsonSchemaMixin):
    type: MazeTileType = MazeTileType.NONE


def parse_additional_activities(properties: dict[str, Any]) -> list[Activity]:
    activities: list[Activity] = []

    i = 0
    while True:
        key = f"additional_activity_{i}"

        i += 1
        if key not in properties:
            break

        activities.append(Activity(properties[key]))

    return activities
