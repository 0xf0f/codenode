import io
from typing import Iterator, Tuple

from .node import Node


class Writer:
    def process_node(self, node: Node) -> Node:
        return node

    def node_to_lines(self, node: Node) -> Iterator[Tuple[int, str]]:
        node = self.process_node(node)
        stack = [(node, 0, node.total())]

        while stack:
            node, depth, iterator = stack[-1]

            try:
                item = next(iterator)

            except StopIteration:
                stack.pop()
                continue

            if isinstance(item, Node):
                item = self.process_node(item)
                stack.append(
                    (
                        item,
                        depth+node.child_depth_offset,
                        item.total()
                    )
                )

            else:
                yield depth, item

    def dump(
            self,
            node: Node,
            stream,
            indent: str = None,
            base_depth=0
    ) -> None:
        if indent is None:
            indent = '    '

        for depth, line in self.node_to_lines(node):
            stream.write(indent*(depth+base_depth))
            stream.write(line)
            stream.write('\n')

    def dumps(
            self,
            node: Node,
            indent: str = None,
            base_depth=0
    ) -> str:
        string_io = io.StringIO()
        self.dump(node, string_io, indent, base_depth)
        return string_io.getvalue()
