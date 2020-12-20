import io
from codenode.base import CodeNode
from typing import Union

DumpStream = Union[io.StringIO, io.TextIOBase]


class CodeNodeWriter:
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
            indent=None,
            base_depth=0
    ):
        if indent is None:
            from codenode.util.constants import default_indent
            indent = default_indent

        for depth, line in node.to_lines():
            stream.write(indent*(depth+base_depth))
            stream.write(line)
            stream.write('\n')

    def dumps(
            self,
            node: CodeNode,
            indent=None,
            base_depth=0
    ):
        string_io = io.StringIO()
        self.dump(node, string_io, indent, base_depth)
        return string_io.getvalue()


default_writer = CodeNodeWriter()
