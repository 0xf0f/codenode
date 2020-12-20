import io
from codenode.base import CodeNode
from typing import Union
from codenode.functionality.constants import default_indent

DumpStream = Union[io.StringIO, io.TextIOBase]


class CodeNodeWriter:
    def __init__(self):
        pass

    def node_to_lines(self, node: CodeNode):
        stack = [(node, 0, node.total())]

        while stack:
            node, depth, iterator = stack[-1]

            try:
                item = next(iterator)

            except StopIteration:
                stack.pop()
                continue

            if isinstance(item, CodeNode):
                stack.append(
                    (item, depth+node.child_depth_offset, item.total())
                )

            else:
                yield depth, item

    def dump(
            self,
            node: CodeNode,
            stream: DumpStream,
            base_depth=0
    ):
        for depth, line in node.to_lines():
            stream.write(indent*(depth+base_depth))
            stream.write(line)
            stream.write('\n')

    def dumps(
            self,
            node: CodeNode,
            indent=default_indent,
            base_depth=0
    ):
        string_io = io.StringIO()
        self.dump(node, string_io, indent, base_depth)
        return string_io.getvalue()


writer = CodeNodeWriter()
