import inspect
from typing import Any, List, Tuple

from src.lib.parser.combinator import PNode


class Transformer:

    def __init__(self):
        self.__transformers = self.__collect_transformers()

    def __collect_transformers(self):
        return {
            name: val
            for name, val in inspect.getmembers(self)
            if not name.startswith("_")
        }

    def __transform(self, node: PNode, before: bool = False) -> Any:
        name = str(node.type)
        if before:
            return tr(node) \
                if (tr := self.__transformers.get(f"before_{name}", None)) \
                else node

        return tr(*node.values) \
            if (tr := self.__transformers.get(name, None)) is not None \
            else node

    def __call__(self, tree):
        if isinstance(tree, List | Tuple):
            return [self(i) for i in tree]
        if isinstance(tree, PNode):
            node = self.__transform(tree, before=True)
            node = PNode(node.type, self(node.values))
            return self.__transform(node)
        return tree
