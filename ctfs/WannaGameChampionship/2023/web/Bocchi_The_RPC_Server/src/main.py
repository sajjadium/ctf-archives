from typing import Generator

from rpcpy import RPC
from typing_extensions import TypedDict

app = RPC()


@app.register
def none() -> None:
    return


@app.register
def sayhi(name: str) -> str:
    return f"Hello {name} from Bocchi the Rock!"


@app.register
def yield_data(max_num: int) -> Generator[int, None, None]:
    for i in range(max_num):
        yield i


D = TypedDict("D", {"key": str, "other-key": str})


@app.register
def query_dict(value: str) -> D:
    return {"key": value, "other-key": value}
