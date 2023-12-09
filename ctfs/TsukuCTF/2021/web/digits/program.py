from typing import Optional
from fastapi import FastAPI
import random

app = FastAPI()

FLAG = "TsukuCTF{}"


@app.get("/")
def main(q: Optional[str] = None):
    if q == None:
        return {
            "msg": "please input param 'q' (0000000000~9999999999).  example: /?q=1234567890"
        }
    if len(q) != 10:
        return {"msg": "invalid query"}
    if "-" in q or "+" in q:
        return {"msg": "invalid query"}
    try:
        if not type(int(q)) is int:
            return {"msg": "invalid query"}
    except:
        return {"msg": "invalid query"}

    you_are_lucky = 0

    for _ in range(100):
        idx = random.randrange(4)
        if q[idx] < "0":
            you_are_lucky += 1
        if q[idx] > "9":
            you_are_lucky += 1

    if you_are_lucky > 0:
        return {"flag": FLAG}
    else:
        return {"msg": "Sorry... You're unlucky."}
