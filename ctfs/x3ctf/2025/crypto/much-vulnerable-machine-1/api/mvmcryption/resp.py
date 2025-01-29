from __future__ import annotations

from fastapi import HTTPException, status

PERMISSION_DENIED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied.",
)


def not_found(model: object) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{model.__name__} not found.",
    )
