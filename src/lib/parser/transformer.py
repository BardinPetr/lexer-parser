import inspect
from typing import Iterable, Any, List, Tuple

from src.lib.parser.parser import PNode


class Transformer:

    def __init__(self):
        self._transformers = self._collect_transformers()

    def _collect_transformers(self):
        return {
            name: val
            for name, val in inspect.getmembers(self)
            if not name.startswith("_")
        }

    def _transform(self, node: PNode, before: bool = False) -> Any:
        if before:
            tr = self._transformers.get(f"before_{node.type.name}", None)
            return node if tr is None else tr(node)

        tr = self._transformers.get(node.type.name, None)
        return node if tr is None else tr(*node.values)

    def __call__(self, tree):
        if isinstance(tree, List | Tuple):
            return [self(i) for i in tree]
        if isinstance(tree, PNode):
            node = self._transform(tree, before=True)
            node = PNode(node.type, self(node.values))
            return self._transform(node)
        return tree
