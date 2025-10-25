from __future__ import annotations

import json
import sys
from typing import Any, Callable, Dict, List
import os

from ind_cpa_d_bitwise_game import (
    AddCircuit,
    BitwiseCKKSIndCpaDGame,
    HomomorphicCKKSFunction,
    MultiplyCircuit,
    SquareCircuit,
)

flag = os.environ.get("FLAG", "ptm{REDACTED}")

CIRCUIT_FACTORIES: Dict[str, Callable[[], HomomorphicCKKSFunction]] = {
    "square": SquareCircuit,
    "add": AddCircuit,
    "sum": AddCircuit,
    "mul": MultiplyCircuit,
    "multiply": MultiplyCircuit,
}


class INDCPADServer:
    """Simple line-oriented server exposing the IND-CPA-D oracles to a client."""

    def __init__(
        self,
        *,
        mult_depth: int = 2,
        scale_mod_size: int = 50,
        bit_length: int = 64,
    ) -> None:
        self.game = BitwiseCKKSIndCpaDGame(
            mult_depth=mult_depth,
            scale_mod_size=scale_mod_size,
            batch_size=1,
            bit_length=bit_length,
        )
        self._resolved = False

    # ------------------------------------------------------------------ #
    # Public API

    def encrypt(self, m0: float, m1: float) -> Dict[str, Any]:
        ciphertext = self.game.enc_oracle(m0, m1)
        index = len(self.game.state) - 1
        return {"status": "ok", "state_index": index}

    def eval(self, function: str, indices: List[int]) -> Dict[str, Any]:
        circuit = self._resolve_circuit(function)
        self.game.eval_oracle(tuple(indices), circuit)
        index = len(self.game.state) - 1
        return {"status": "ok", "state_index": index}

    def decrypt(self, index: int, position: int) -> Dict[str, Any]:
        bit = self.game.dec_oracle(index, position)
        if bit is None:
            return {"status": "denied", "reason": "bit-mismatch"}
        return {"status": "ok", "bit": int(bit)}

    def guess(self, bit: int) -> Dict[str, Any]:
        if self._resolved:
            return {"status": "error", "error": "game already resolved"}

        self._resolved = True
        if (bit & 1) == self.game.challenge_bit:
            return {"status": "ok", "result": "WIN"}
        return {"status": "ok", "result": "LOSE"}

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        command = request.get("command")
        if command is None:
            raise ValueError("missing command field")

        command = str(command).lower()
        if command == "encrypt":
            return self.encrypt(float(request["m0"]), float(request["m1"]))
        if command == "eval":
            function = str(request["function"])
            indices = [int(idx) for idx in request["indices"]]
            return self.eval(function, indices)
        if command == "decrypt":
            return self.decrypt(int(request["index"]), int(request["position"]))
        if command == "guess":
            return self.guess(int(request["bit"]))

        raise ValueError(f"unknown command '{command}'")

    # ------------------------------------------------------------------ #
    # Helpers

    @staticmethod
    def _resolve_circuit(descriptor: str) -> HomomorphicCKKSFunction:
        keyword = descriptor.lower()
        builder = CIRCUIT_FACTORIES.get(keyword)
        if builder is None:
            raise ValueError(f"unsupported circuit '{descriptor}'")
        return builder()


def main() -> None:
    rounds = 100

    for current_round in range(1, rounds + 1):
        server = INDCPADServer()
        print(json.dumps({"status": "new_round", "round": current_round}))
        sys.stdout.flush()

        while True:
            line = sys.stdin.readline()
            if not line:
                return
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                print(json.dumps({"status": "error", "error": "invalid json"}))
                sys.stdout.flush()
                continue

            try:
                response = server.handle_request(request)
            except Exception as exc:
                response = {"status": "error", "error": str(exc)}

            print(json.dumps(response))
            sys.stdout.flush()

            result = response.get("result")
            if result == "WIN":
                break
            if result == "LOSE":
                return

    print(json.dumps({"status": "ok", "flag": flag}))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
