from base64 import urlsafe_b64decode, urlsafe_b64encode


def encode(content: bytes | str) -> str:
    def _encode():
        if isinstance(content, str):
            return urlsafe_b64encode(content.encode()).decode()
        return urlsafe_b64encode(content).decode()

    return _encode().replace("=", "")


def decode(content: str | bytes) -> bytes:
    rem = len(content) % 4

    if rem > 0:
        try:
            content += b"=" * (4 - rem)
        except Exception:
            content += "=" * (4 - rem)

    if isinstance(content, str):
        return urlsafe_b64decode(content.encode())
    return urlsafe_b64decode(content)


def chunk(stuff: bytes):
    """Chunk stuff into 16 byte blocks."""

    assert len(stuff)
    assert len(stuff) % 16 == 0
    blocks = []
    for i in range(0, len(stuff), 16):
        blocks.append(stuff[i : i + 16])
    return blocks
