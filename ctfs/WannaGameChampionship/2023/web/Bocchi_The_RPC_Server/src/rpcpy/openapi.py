from __future__ import annotations

import functools
import inspect
import typing
import warnings

__all__ = [
    "create_model",
    "validate_arguments",
    "set_type_model",
    "is_typed_dict_type",
    "parse_typed_dict",
    "TEMPLATE",
]

Callable = typing.TypeVar("Callable", bound=typing.Callable)

try:
    from pydantic import BaseModel, ValidationError, create_model
    from pydantic import validate_arguments as pydantic_validate_arguments

    # visit this issue
    # https://github.com/samuelcolvin/pydantic/issues/1205
    def validate_arguments(function: Callable) -> Callable:
        function = pydantic_validate_arguments(function)

        @functools.wraps(function)
        def change_exception(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except ValidationError as exception:
                type_error = TypeError(
                    "Failed to pass pydantic's type verification, please output"
                    " `.more_info` of this exception to view detailed information."
                )
                type_error.more_info = exception
                raise type_error

        return change_exception  # type: ignore

except ImportError:

    def create_model(*args, **kwargs):  # type: ignore
        raise NotImplementedError("Need install `pydantic` from pypi.")

    def validate_arguments(function: Callable) -> Callable:
        return function

    class ValidationError(Exception):  # type: ignore
        """
        Just for import
        """

    if typing.TYPE_CHECKING:
        from pydantic import BaseModel


def set_type_model(func: Callable) -> Callable:
    """
    try generate request body model from type hint and default value
    """
    sig = inspect.signature(func)
    field_definitions: typing.Dict[str, typing.Any] = {}
    for name, parameter in sig.parameters.items():
        if parameter.annotation == parameter.empty:
            # raise ValueError(
            #     f"You must specify the type for the parameter {func.__name__}:{name}."
            # )
            return func  # Maybe the type hint should be mandatory? I'm not sure.
        if parameter.default == parameter.empty:
            field_definitions[name] = (parameter.annotation, ...)
        else:
            field_definitions[name] = (parameter.annotation, parameter.default)
    if field_definitions:
        try:
            body_model: typing.Type[BaseModel] = create_model(
                func.__name__, **field_definitions
            )
            setattr(func, "__body_model__", body_model)
        except NotImplementedError:
            message = (
                "If you wanna using type hint "
                "to create OpenAPI docs or convert type, "
                "please install `pydantic` from pypi."
            )
            warnings.warn(message, ImportWarning)
    return func


def is_typed_dict_type(type_) -> bool:
    return (
        isinstance(type_, type)
        and issubclass(type_, dict)
        and getattr(type_, "__annotations__", False)
    )


def parse_typed_dict(typed_dict) -> typing.Type[BaseModel]:
    """
    parse `TypedDict` to generate `pydantic.BaseModel`
    """
    annotations = {}
    for name, field in typed_dict.__annotations__.items():
        if is_typed_dict_type(field):
            annotations[name] = (parse_typed_dict(field), ...)
        else:
            default_value = getattr(typed_dict, name, ...)
            annotations[name] = (field, default_value)

    return create_model(typed_dict.__name__, **annotations)  # type: ignore


TEMPLATE = """<!DOCTYPE html>
<html>

<head>
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.30.0/swagger-ui.css">
    <title>OpenAPI Docs</title>
</head>

<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.30.0/swagger-ui-bundle.js"></script>
    <script>
        const ui = SwaggerUIBundle({
            url: './get-openapi-docs',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
            layout: "BaseLayout",
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true
        })

    </script>
</body>

</html>
"""
