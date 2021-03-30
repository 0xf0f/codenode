from typing import List, Tuple, Union, Iterator
from .settings import settings
from .constants import HasStringWriteMethod
from .constants import NodeArgumentType


class Node:
    child_depth_offset = 1

    def __init__(self):
        self.children: List[Node] = []

    def header(self) -> Iterator[Union['Node', str]]:
        yield from ()

    def body(self) -> Iterator[Union['Node', str]]:
        yield from self.children

    def footer(self) -> Iterator[Union['Node', str]]:
        yield from ()

    def total(self) -> Iterator[Union['Node', str]]:
        yield from self.header()
        yield from self.body()
        yield from self.footer()

    def add_child(self, child: NodeArgumentType) -> 'Node':
        if isinstance(child, str):
            child = Line(child)

        elif isinstance(child, (list, tuple)):
            node = Node()
            node.add_children(*child)
            child = node

        self.children.append(child)
        return child

    def add_children(self, *children: NodeArgumentType):
        for child in children:
            self.add_child(child)

    def to_lines(self) -> Iterator[Tuple[int, str]]:
        yield from settings.default_writer.node_to_lines(self)

    def dump(self, stream: HasStringWriteMethod, indent: str = None, base_depth=0):
        return settings.default_writer.dump(self, stream, indent, base_depth)

    def dumps(self, indent: str = None, base_depth=0) -> str:
        return settings.default_writer.dumps(self, indent, base_depth)

    def walk(self, yield_self=False) -> Iterator[Union['Node', str]]:
        if yield_self:
            stack = [self]
        else:
            stack = [*self.children]

        while stack:
            item = stack.pop()
            yield item
            stack.extend(item.children)

    def __call__(self, *children: NodeArgumentType):
        self.add_children(*children)
        return self


class Line(Node):
    def __init__(self, content=''):
        super().__init__()

        self.content = content

    def header(self):
        yield self.content

