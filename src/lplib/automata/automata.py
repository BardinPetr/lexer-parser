from typing import Dict, Generic, TypeVar, Optional, Tuple, List, Iterable

from lplib.automata.state import AutomataStateId, AutomataState

ST = TypeVar("ST")
TR = TypeVar("TR")
V = TypeVar("V")


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
            is_terminal = i == (len(key) - 1)
            cond = key[i]

            existing_id = cur_state.transition(cond)
            if existing_id is not None:
                cur_state = self.state_by_id(existing_id)
                if is_terminal:
                    cur_state.make_terminal(value)
                continue

            next_state = self._create_state_after(
                cur_state.id,
                cond,
                terminal=value if is_terminal else None
            )

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
        Search for key in trie. Return the longest variant
        :param key: iterable of conditions
        :return:    if found: matched values list and terminal node contents, else: None
        """
        cur_state = self.initial_state

        matched = []
        for cond in key:
            next_state = self.state_by_id(cur_state.transition(cond))
            if next_state is None:
                break
            matched.append(cond)
            cur_state = next_state

        if cur_state is not None and cur_state.is_terminal():
            return matched, cur_state.value
        return None


class StringAutomata(Generic[V], Automata[str, V]):

    def search(self, key: Iterable[TR]) -> Optional[Tuple[str, V]]:
        res = super().search(key)
        if res is None:
            return res

        return ''.join(res[0]), res[1]
