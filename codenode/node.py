from typing import List, Union


class Node:
    child_depth_offset = 1

    def __init__(self):
        self.children: List[Node] = []

    def header(self):
        yield from ()

    def body(self):
        yield from self.children

    def footer(self):
        yield from ()

    def total(self):
        yield from self.header()
        yield from self.body()
        yield from self.footer()

    def add_child(self, child: Union[str, 'Node']):
        if isinstance(child, str):
            from .line import Line
            child = Line(child)

        elif isinstance(child, (list, tuple)):
            node = Node()
            node.add_children(*child)
            child = node

        self.children.append(child)

    # def remove_child(self, child: 'Node'):
    #     self.children.remove(child)

    def add_children(self, *children: Union[str, 'Node']):
        for child in children:
            self.add_child(child)

    def to_lines(self):
        from . import default_writer
        yield from default_writer.node_to_lines(self)

    def dump(self, stream, indent=None, base_depth=0):
        from . import default_writer
        return default_writer.dump(self, stream, indent, base_depth)

    def dumps(self, indent=None, base_depth=0):
        from . import default_writer
        return default_writer.dumps(self, indent, base_depth)

    def walk(self, yield_self=False):
        if yield_self:
            stack = [self]
        else:
            stack = [*self.children]

        while stack:
            item = stack.pop()
            yield item
            stack.extend(item.children)

    def __call__(self, *children: Union[str, 'Node']):
        self.add_children(*children)
        return self
