from typing import List, Union

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
        yield from self.children

    def footer(self):
        yield from ()

    def total(self):
        yield from self.header()
        yield from self.body()
        yield from self.footer()

    def add_child(self, child: Union[str, 'CodeNode']):
        if isinstance(child, str):
            from .line import Line
            child = Line(child)
        self.children.append(child)

    # def remove_child(self, child: 'CodeNode'):
    #     self.children.remove(child)

    def add_children(self, *children: Union[str, 'CodeNode']):
        for child in children:
            self.add_child(child)

    def to_lines(self):
        from codenode.base import default_writer
        yield from default_writer.node_to_lines(self)

    def dump(self, stream, indent=None, base_depth=0):
        from codenode.base import default_writer
        return default_writer.dump(self, stream, indent, base_depth)

    def dumps(self, indent=None, base_depth=0):
        from codenode.base import default_writer
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

    def __call__(self, *children: Union[str, 'CodeNode']):
        self.add_children(*children)
        return self
