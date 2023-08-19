import asyncio
import os
import random
import secrets
import string
from typing import Iterable, Optional, Tuple


def random_string(length: int) -> str:
    allchar = string.ascii_letters + string.digits
    return "".join(secrets.choice(allchar) for x in range(length))


def random_transaction_id() -> bytes:
    return os.urandom(12)


async def create_datagram_endpoint(protocol_factory,
    remote_addr: Tuple[str, int] = None,
    local_address: str = None,
    local_ports: Optional[Iterable[int]] = None,
):
    """
    Asynchronousley create a datagram endpoint.

    :param protocol_factory: Callable returning a protocol instance.
    :param remote_addr: Remote address and port.
    :param local_address: Local address to bind to.
    :param local_ports: Set of allowed local ports to bind to.
    """
    if local_ports is not None:
        ports = list(local_ports)
        random.shuffle(ports)
    else:
        ports = (0,)
    loop = asyncio.get_event_loop()
    for port in ports:
        try:
            print(ports)
            transport, protocol = await loop.create_datagram_endpoint(
                protocol_factory, remote_addr=remote_addr, local_addr=(local_address, port)
            )
            return transport, protocol
        except OSError as exc:
            if port == ports[-1]:
                # this was the last port, give up
                raise exc
    raise ValueError("local_ports must not be empty")
