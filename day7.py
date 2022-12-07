from textwrap import indent
from typing import Generator

# really just here for the type hinting
class FSO: # FSO: FileSystemObject
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def size(self) -> int:
        return self._size

class File(FSO):
    def __init__(self, size: str, name: str) -> None:
        self._size = int(size)
        self._name = name
    
    def __repr__(self) -> str:
        return f"- {self.name} (file, size={self.size})"

class Directory(FSO):
    def __init__(self, name: str) -> None:
        self._name = name
        self.contents: dict[str, FSO] = {}
    
    def add(self, child: FSO) -> None:
        self.contents[child.name] = child
    
    # couldn't figure out how to get the type hinting correct on this one
    # for some reason can't type hint Generator[Directory, None, None]
    @property
    def dirs(self) -> Generator[FSO, None, None]:
        yield self
        for gen in [child.dirs for child in self.contents.values() if type(child)==Directory]:
            yield from gen
    
    @property
    def dir_sizes(self):
        return (i.size for i in self.dirs)
    
    @property
    def _size(self) -> int:
        return sum(child.size for child in self.contents.values())
    
    def __repr__(self) -> str:
        children = '\n'.join(indent(str(child), ' '*2)
                             for child in self.contents.values())
        return f"- {self.name} (dir)\n{children}"

class Filesystem:
    def __init__(self) -> None:
        self.root: Directory        = Directory("/")
        self.head: list[Directory]  = [self.root] # (c/sh)ould be a doubly-linked list
    
    @property
    def tail(self) -> Directory:
        assert len(self.head)>0 # sanity check
        return self.head[-1]

    def cd(self, name: str) -> None:
        match name:
            case "/": # jump to root
                self.head = [self.root]
            case "..": # up one
                assert len(self.head)>1 # sanity check
                self.head.pop()
            case _: # everything else is a cd-into-child
                assert name in self.tail.contents.keys() # sanity check
                self.head.append(self.tail.contents[name])
    
    def __repr__(self) -> str:
        return str(self.root)

def parse(lines: list[str]) -> Filesystem:
    fs = Filesystem()
    for line in lines:
        if line[0]=="$": # the line is a command, either `ls` or `cd`
            match line[2:4]:
                case "cd":
                    fs.cd(line.split(" ")[-1])
                case "ls":
                    pass # falls through to the else block on next line
                case _: # sanity check
                    raise ValueError(f"command {line[2:]} not in (`ls`, `cd`)")
        else: # the line is a result from an `ls` command
            item = line.split(" ")
            assert len(item)==2 # sanity check
            left, right = item
            match left:
                case "dir":
                    fs.tail.add(Directory(right))
                case _:
                    fs.tail.add(File(left, right))
    return fs

with open("input7.txt") as f:
    lines = [line.strip() for line in f]
fs = parse(lines)

print(sum(filter(lambda x: x <= 1e5,                    fs.root.dir_sizes))) # part 1
print(min(filter(lambda x: x > fs.root.size - int(4e7), fs.root.dir_sizes))) # part 2