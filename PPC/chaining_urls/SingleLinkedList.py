from typing import Generator, TypeVar


T = TypeVar("T")


class SingleLinkedList[T](dict[T,T]):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.start: T
        self.end: T

    def add(self, value: T):
        if len(self) == 0:
            self.start = value
            self.end = value
        self[value] = self.start
        self[self.end] = value
        self.end = value

    def traverse(self) -> Generator:
        i: T = self.start
        while True:
            yield i, self[i]
            i = self[i]
            if i == self.start:
                return

    def pprint(self) -> None:
        for i,(k,v) in enumerate(self.traverse()):
            print(f"{i}: ({k}: {v})")

