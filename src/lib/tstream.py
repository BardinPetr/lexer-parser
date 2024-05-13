from typing import Callable


class CharStream:
    def __init__(self, text):
        self._text = text
        self._pos = 0

    def peek(self) -> str:
        return self._text[self._pos]

    def advance(self, cnt: int = 1):
        self._pos += cnt

    def next(self) -> str:
        res = self._text[self._pos]
        self.advance()
        return res

    def skip(self, skip_while: Callable[[str], bool]):
        while not self.eof() and skip_while(self.peek()):
            self.advance()

    def eof(self) -> bool:
        return self._pos >= len(self._text)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._text[self._pos + item]
        if isinstance(item, slice):
            if any([item.stop, item.step]):
                raise NotImplementedError("Only [:] and [start:] slices supported")
            if item.start:
                return self._text[self._pos + item.start:]
            return self._text[self._pos:]


class FileCharStream(CharStream):
    def __init__(self, filepath):
        with open(filepath, "r") as f:
            super().__init__(f.read())
