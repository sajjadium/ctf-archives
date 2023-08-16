import hashlib
import json
from typing import Any

from dataclasses_jsonschema import JsonSchemaMixin

from server.game.map.properties import *  # type: ignore


def get_class(name: str, properties: dict[str, Any]) -> dict[str, dict[str, Any]]:
    m = hashlib.md5()
    m.update(name.encode())
    id = int(m.hexdigest(), 16)

    member_types = {}
    members = []

    for n, p in properties["properties"].items():
        propertyType = None
        default = None
        type = None

        if "type" in p:
            match p["type"]:
                case "string":
                    type = "string"
                case "integer":
                    type = "int"
                case "boolean":
                    type = "bool"
                case "number":
                    type = "float"
                case _:
                    raise NotImplementedError(p["type"])

            assert "default" in p, p
        elif "$ref" in p:
            ref = p["$ref"]
            ref = ref.rsplit("/", 1)[1]

            type = "class"
            default = {}
            propertyType = ref
        elif "type_" in p:
            match p["type_"]:
                case "object":
                    type = "object"
                case _:
                    raise NotImplementedError(p["type_"])

        if "default" in p:
            default = p["default"]

        assert type is not None
        assert default is not None

        member: dict[str, Any] = {
            "name": n,
            "type": type,
            "value": default,
        }

        if "enum" in p:
            m = hashlib.md5()
            m.update(n.encode())
            member_types[n] = {
                "id": int(m.hexdigest(), 16),
                "name": n.title(),
                "storageType": "string",
                "type": "enum",
                "values": p["enum"],
            }

            propertyType = n.title()

        if propertyType:
            member["propertyType"] = propertyType

        members.append(member)

    property_types = {
        name: {
            "id": id,
            "name": name.title(),
            "type": "class",
            "useAs": [
                "property",
                "map",
                "layer",
                "object",
                "tile",
                "tileset",
                "wangcolor",
                "wangset",
            ],
            "color": "#ffa0a0a4",
            "drawFill": True,
            "members": members,
        }
    }
    property_types |= member_types

    return property_types


def parse_properties(
    name: str, properties: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    match properties["type"]:
        case "object":
            return get_class(name, properties)
        case _:
            raise NotImplementedError()


properties = JsonSchemaMixin.all_json_schemas()

property_types: dict[str, Any] = {}

for key, value in properties.items():
    if "type" in value:
        property_types |= parse_properties(key, value)
    elif "allOf" in value:
        value = value["allOf"]
        ref = value[0]["$ref"]
        ref = ref.rsplit("/", 1)[1]

        assert ref in property_types
        property_types |= parse_properties(key, value[1])
        property_types[key]["members"] += property_types[ref]["members"]
    else:
        raise NotImplementedError()


with open("src/server/server/map/map.tiled-project", "r") as f:
    tiled_project = json.load(f)

tiled_project["propertyTypes"] = list(property_types.values())
# print(json.dumps(tiled_project))

with open("src/server/server/map/map.tiled-project", "w") as f:
    json.dump(obj=tiled_project, fp=f, indent=4)
