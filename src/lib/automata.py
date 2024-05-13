from dataclasses import dataclass
from typing import Dict, Generic, TypeVar, Optional, Tuple, List, Iterable

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
        return self._transitions.get(trans_condition, None)


class Automata(Generic[ST, V]):

    def __init__(self):
        self._states: Dict[AutomataStateId[TR], AutomataState[TR, V]] = {}

        initial_state_id = AutomataStateId(tuple())
        self.initial_state = AutomataState(initial_state_id)
        self._states[initial_state_id] = self.initial_state

    def state_by_id(self, item: AutomataStateId) -> Optional[AutomataState[TR, V]]:
        return self._states.get(item, None)

    def _create_state_after(self, sid: AutomataStateId[TR], cond: TR, terminal: Optional[V]) -> AutomataState[TR, V]:
        sid = AutomataStateId[TR]((*sid.value, cond))
        self._states[sid] = AutomataState(sid, terminal)
        return self._states[sid]

    def push_state(self, key: List[TR], value: ST):
        cur_state = self.initial_state
        for i in range(len(key)):
            cond = key[i]
            existing_id = cur_state.transition(cond)
            if existing_id is not None:
                cur_state = self.state_by_id(existing_id)
                continue

            terminal = value if (len(key) - 1) == i else None
            next_state = self._create_state_after(cur_state.id, cond, terminal)

            cur_state.add_transition(cond, next_state.id)
            cur_state = next_state

    def print_words(self, cur: AutomataState[TR, V] = None, order=None):
        if order is None:
            order = []
        if cur is None:
            cur = self.initial_state

        if cur.is_terminal():
            print(f"{''.join(order)} -> {cur.value}")

        for k, v in cur.transitions:
            self.print_words(self.state_by_id(v), order + [k])

    def search(self, key: Iterable[TR]) -> Optional[Tuple[List[TR], V]]:
        """
        Search for key in trie. Return
        :param key: iterable of conditions
        :return:    if found: matched values list and terminal node contents, else: None
        """
        cur_state = self.initial_state

        for cond in key:
            next_state = self.state_by_id(cur_state.transition(cond))
            if next_state is None:
                break
            cur_state = next_state

        if cur_state is not None and cur_state.is_terminal():
            return list(cur_state.id.value), cur_state.value
        return None


class StringAutomata(Generic[V], Automata[str, V]):

    def search(self, key: Iterable[TR]) -> Optional[Tuple[str, V]]:
        res = super().search(key)
        if res is None:
            return res

        return ''.join(res[0]), res[1]
