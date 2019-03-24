import io
from typing import List, Tuple

codenode_subclasses = {}


class CodeNode:
    # defaults = {}
    child_depth_offset = 1

    def __init__(self):
        self.children: List[CodeNode] = []

    # def __init_subclass__(cls, **kwargs):
    #     super().__init_subclass__(**kwargs)
    #     codenode_subclasses[f'{cls.__module__}.{cls.__qualname__}'] = cls
    #
    #     for key, value in cls().__dict__.items():
    #         cls.defaults[key] = value

    def header(self):
        yield from ()

    def body(self):
        yield from ()

    def footer(self):
        yield from ()

    def total(self):
        yield from self.header()
        yield from self.body()
        yield from self.footer()

    def add_child(self, child: 'CodeNode'):
        self.children.append(child)

    # def remove_child(self, child: 'CodeNode'):
    #     self.children.remove(child)

    def to_lines(self):
        from base import writer
        yield from writer.node_to_lines(self)

    def dump(self, stream, indent='    ', base_depth=0):
        from base import writer
        return writer.dump(self, stream, indent, base_depth)

    def dumps(self, indent='    ', base_depth=0):
        from base import writer
        return writer.dumps(self, indent, base_depth)

