import io
from .node import Node
from typing import Union
from .settings import settings

DumpStream = Union[io.StringIO, io.TextIOBase]


class CodeNodeWriter:
    def node_to_lines(self, node: Node):
        stack = [(node, 0, node.total())]

        while stack:
            node, depth, iterator = stack[-1]

            try:
                item = next(iterator)

            except StopIteration:
                stack.pop()
                continue

            if isinstance(item, Node):
                stack.append(
                    (item, depth+node.child_depth_offset, item.total())
                )

            else:
                yield depth, item

    def dump(
            self,
            node: Node,
            stream: DumpStream,
            indent: str = None,
            base_depth=0
    ):
        if indent is None:
            indent = settings.default_indent

        for depth, line in node.to_lines():
            stream.write(indent*(depth+base_depth))
            stream.write(line)
            stream.write('\n')

    def dumps(
            self,
            node: Node,
            indent=None,
            base_depth=0
    ):
        string_io = io.StringIO()
        self.dump(node, string_io, indent, base_depth)
        return string_io.getvalue()
