from textwrap import indent
from itertools import chain
from typing import Iterable, Generator, Self


class File:
    def __init__(self, size: str, name: str) -> None:
        self.size = int(size)
        self.name = name

    def __repr__(self) -> str:
        return f"- {self.name} (file, size={self.size})"


class Directory:
    def __init__(self, name: str) -> None:
        self.name = name
        self.contents: dict[str, File | Directory] = {}

    @property
    def dirs(self) -> Generator[Self, None, None]:  # type: ignore
        yield self
        yield from chain.from_iterable(
            child.dirs for child in self.contents.values() if type(child) == Directory
        )

    @property
    def size(self) -> int:
        return sum(child.size for child in self.contents.values())

    def __repr__(self) -> str:
        children = "\n".join(
            indent(str(child), " " * 2) for child in self.contents.values()
        )
        return f"- {self.name} (dir)\n{children}"


class Filesystem:
    def __init__(self) -> None:
        self.root = Directory("/")
        self.head: list[Directory] = [self.root]

    def cd(self, name: str) -> None:
        match name:
            case "/":  # jump to root
                self.head = [self.root]
            case "..":  # up one
                self.head.pop()
            case _:  # everything else is a cd-into-child
                child = self.head[-1].contents[name]
                assert type(child) == Directory
                self.head.append(child)

    def __repr__(self) -> str:
        return str(self.root)


def build(lines: Iterable[str], fs: Filesystem) -> Filesystem:
    for line in lines:
        if line[0:4] == "$ cd":
            fs.cd(line[5:])
        elif line[0] != "$":
            child: File | Directory = (
                Directory(data[1])
                if (data := line.split(" "))[0] == "dir"
                else File(*data)
            )
            fs.head[-1].contents[child.name] = child
    return fs


with open("input7.txt") as f:
    fs = build((line.strip() for line in f), Filesystem())

print(sum(x.size for x in fs.root.dirs if x.size <= 1e5))  # type: ignore
print(min(x.size for x in fs.root.dirs if x.size > fs.root.size - 4e7))  # type: ignore
