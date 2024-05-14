from dataclasses import dataclass
from typing import Generic, Tuple, Optional, Dict, TypeVar, Callable

ST = TypeVar("ST")
TR = TypeVar("TR")
V = TypeVar("V")


@dataclass
class AutomataStateId(Generic[TR]):
    value: Tuple[TR]

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, __o: 'AutomataStateId'):
        return self.value == __o.value


class AutomataState(Generic[TR, V]):
    def __init__(self, sid: AutomataStateId[TR], terminal: Optional[V] = None):
        self._id = sid
        self._value = terminal
        self._transitions: Dict[TR, AutomataStateId['TR']] = {}
        self._fallback_transitions: Dict[Callable[['TR'], bool], AutomataStateId['TR']] = {}

    def is_terminal(self) -> bool:
        return self._value is not None

    @property
    def id(self) -> AutomataStateId[TR]:
        return self._id

    @property
    def transitions(self):
        return self._transitions.items()

    @property
    def value(self) -> Optional[V]:
        return self._value

    def add_transition(self, condition: TR, target_id: AutomataStateId[TR]):
        sid = self._transitions.get(condition, None)
        if sid is None:
            self._transitions[condition] = target_id

    def transition(self, trans_condition: TR) -> Optional[AutomataStateId['TR']]:
        sid = self._transitions.get(trans_condition, None)
        if sid is None:
            for check, sid_next in self._fallback_transitions:
                if check(trans_condition):
                    return sid_next
        return sid

    def make_terminal(self, term_value: V):
        self._value = term_value
