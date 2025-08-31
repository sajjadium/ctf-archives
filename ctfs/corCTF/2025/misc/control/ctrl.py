#!/usr/bin/env python3
import struct

import numba
import numpy as np
import wasmtime
import base64
import tempfile
import sys

from scipy.integrate import solve_ivp

LOAD_RESISTANCE = 5
SOURCE_RESISTANCE = 0.01
SOURCE_VOLTAGE = 15

C1 = 47e-6
C2 = 47e-6
L = 88e-6

DT = 0.0001
N = 1000

@numba.njit
def F(x, u):
    vC1 = x[0] + np.random.normal(0, 0.1)
    vC2 = x[1] + np.random.normal(0, 0.1)
    i_L = x[2] + np.random.normal(0, 0.1)

    v_L = vC1 * u[0] - vC2 * u[1]
    i_C1 = -u[0] * i_L + (SOURCE_VOLTAGE - vC1) / SOURCE_RESISTANCE
    i_C2 = u[1] * i_L - vC2 / LOAD_RESISTANCE

    dC1 = i_C1 / C1
    dC2 = i_C2 / C2
    di_L = (v_L ) / L

    return np.array([dC1, dC2, di_L])

def unpack_pair_u64_to_float32(u64: int) -> tuple[float, float]:
    b = struct.pack('<Q', u64 & ((1 << 64) - 1))
    u1 = struct.unpack_from('<f', b, 0)[0]
    u0 = struct.unpack_from('<f', b, 4)[0]
    return float(u0), float(u1)

print("enter base64 data: ")
sys.stdout.flush()

# read base64 from stdin
data = input().strip()
decoded = base64.b64decode(data)
temp_wasm = tempfile.NamedTemporaryFile(delete=False, suffix='.wasm')
temp_wasm.write(decoded)
temp_wasm.flush()

engine = wasmtime.Engine()
module = wasmtime.Module.from_file(engine, temp_wasm.name)
store = wasmtime.Store(engine)

class Controller:
    def __init__(self):
        instance = wasmtime.Instance(store, module, [])
        controller_step = instance.exports(store)['controller_step']
        assert isinstance(controller_step, wasmtime.Func)

        self.store = store
        self.controller_step = controller_step

    def step(self, sp: float, x):
        res = self.controller_step(self.store, sp, x[0], x[1], x[2])
        if isinstance(res, tuple):
            res = res[0]
        u0, u1 = unpack_pair_u64_to_float32(int(res))
        wasm_u = np.array([u0, u1], dtype=np.float32)
        return wasm_u


t = np.arange(N+1) * DT
x = np.zeros((N+1, 3))

k = 0

u = np.zeros((N+1, 2))

controller = Controller()
target = np.abs(np.sin(2 * np.pi * 60 * np.arange(N) * DT))

for i in range(N):
    x_prev = x[k]

    local_u = controller.step(target[k], x_prev)
    local_u = np.clip(local_u, 0, 1)
    u[k] = local_u

    sol = solve_ivp(lambda t, x: F(x, local_u), [k * DT, (k + 1) * DT], x_prev)
    x[k + 1] = sol.y.T[-1]
    k += 1

mse = np.mean((x.T[1][5:-1] - target[:len(t)][5:])**2)
if mse < 0.01:
    with open("flag.txt", "r") as f:
        print(f.read().strip())

module.close()
engine.close()
store.close()
temp_wasm.close()