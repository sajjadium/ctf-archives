import sys
import angr
import claripy
import logging

from angr.engines.vex import HeavyVEXMixin
from angr.engines.unicorn import SimEngineUnicorn
from angr.engines.failure import SimEngineFailure
from angr.engines.hook import HooksMixin

class MyEngine(
    SimEngineFailure,
    HooksMixin,
    SimEngineUnicorn,
    HeavyVEXMixin
):
    pass

def solve(filepath):
    proj = angr.Project(filepath, auto_load_libs=False, engine=MyEngine)
    key_bytes = [claripy.BVS(f"key_{i}", 8) for i in range(4)]
    key = claripy.Concat(*key_bytes)

    st = proj.factory.full_init_state(
        args=[filepath, key],
        add_options=angr.options.unicorn,
    )

    for c in key_bytes:
        st.solver.add(c >= ord("A"))
        st.solver.add(c <= ord("Z"))

    sm = proj.factory.simulation_manager(st)
    sm.run()

    print(f"[*] Got {len(sm.deadended)} dead-ended states")

    for state in sm.deadended:
        exit_code = state.regs.eax
        state.add_constraints(state.regs.eax == 0)
        if state.solver.satisfiable():
            return state.solver.eval(key, cast_to=bytes)

    return None


if __name__ == "__main__":
    key = solve(sys.argv[1])
    if key:
        print(f"[*] Key: {key}")
