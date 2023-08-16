from dataclasses import dataclass
from uuid import uuid4

from shared.gen.messages.v1 import Coords
from shared.gen.messages.v1 import Object as ObjectProto
from shared.gen.messages.v1 import ObjectType


@dataclass(kw_only=True)
class Object:
    name: str

    type: ObjectType

    def __init__(
        self,
        x: float,
        y: float,
        direction: float,
        name: str,
        uuid: str | None = None,
        type: ObjectType = ObjectType.OBJECT_TYPE_UNSPECIFIED,
    ) -> None:
        coords = Coords(x=x, y=y, rotation=direction)

        self.name = name

        if uuid is None:
            uuid = str(uuid4())

        self.uuid = uuid
        self.coords = coords
        self.type = type

    async def update(self, dt: float) -> None:
        pass

    @property
    def x(self) -> float:
        return self.coords.x

    @x.setter
    def x(self, x: float) -> None:
        self.coords.x = x

    @property
    def y(self) -> float:
        return self.coords.y

    @y.setter
    def y(self, y: float) -> None:
        self.coords.y = y

    @property
    def direction(self) -> float:
        return self.coords.rotation

    @direction.setter
    def direction(self, direction: float) -> None:
        self.coords.rotation = direction

    def to_proto(self) -> ObjectProto:
        return ObjectProto(
            uuid=self.uuid,
            coords=self.coords,
            type=self.type,
        )
