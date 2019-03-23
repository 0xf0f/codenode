import io
from base.nodes.codenode import CodeNode


class CodeNodeWriter:
    def __init__(self):
        pass

    def node_to_lines(self, node: CodeNode, indent='    ', depth=0):
        stack = [(node, 0, node.total())]

        while stack:
            node, parent_child_depth_offset, iterator = stack[-1]

            try:
                item = next(iterator)

            except StopIteration:
                stack.pop()
                depth -= parent_child_depth_offset
                continue

            if isinstance(item, CodeNode):
                stack.append((item, node.child_depth_offset, item.total()))
                depth += node.child_depth_offset
                continue

            yield f'{indent*depth}{item}'

    def dump(self, node: CodeNode, stream: io.TextIOBase, indent='    ', depth=0):
        for line in self.node_to_lines(node, indent, depth):
            stream.write(line)
            stream.write('\n')

    def dumps(self, node: CodeNode, indent='    ', depth=0):
        string_io = io.StringIO()
        self.dump(node, string_io, indent, depth)
        return string_io.getvalue()
