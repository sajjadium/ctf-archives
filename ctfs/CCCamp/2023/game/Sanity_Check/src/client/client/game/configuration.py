import os
from dataclasses import dataclass, field


@dataclass
class Configuration:
    host: str = field(
        default_factory=lambda: os.environ.get("SERVER_HOST", "localhost")
    )
    port: str = field(default_factory=lambda: os.environ.get("SERVER_PORT", "31337"))
