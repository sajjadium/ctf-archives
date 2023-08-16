from dataclasses import dataclass
from typing import Dict

STATE_CONTINUE = "STATE_CONTINUE"


@dataclass
class BaseState:
    DEBUG = False
    name: str
    parameter: object

    def __init__(self, name: str = "none", param: object = None):
        self.name = name
        self.parameter = param

    def enter(self):
        if BaseState.DEBUG:
            print("Entering state: " + self.name)
        pass

    def leave(self):
        if BaseState.DEBUG:
            print("Entering state: " + self.name)
        pass

    async def update(self, dt: float) -> str:
        return STATE_CONTINUE


@dataclass
class StateMachine:
    current_state: BaseState
    previous_state: BaseState

    _states: Dict[str, BaseState]

    def __init__(self):
        self.current_state = BaseState()
        self.previous_state = BaseState()
        self._states = {}
        pass

    async def update(self, dt: float):
        next_state: str = await self.current_state.update(dt=dt)

        if next_state == STATE_CONTINUE:
            return

        # State transition
        self.change_state(next_state)

    def change_state(self, name: str):
        assert name in self._states.keys(), "State not found: " + name
        self.current_state.leave()

        self.previous_state = self.current_state
        self.current_state = self._states[name]

        self.current_state.enter()

    def add_state(self, state: BaseState):
        assert state.name not in self._states.keys(), (
            "State already in state list" + state.name
        )

        self._states[state.name] = state
