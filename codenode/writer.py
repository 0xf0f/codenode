import typing

from .nodes.newline import Newline
from .nodes.indentation import Indentation
from .nodes.depth_change import DepthChange

if typing.TYPE_CHECKING:
    from typing import Union, Iterable
    NodeType = Iterable[Union[str, 'NodeType']]


class Writer:
    def __init__(
            self,
            node: 'NodeType', *,
            indentation='    ',
            newline='\n',
            depth=0
    ):
        self.node = node
        self.indentation = indentation
        self.newline = newline
        self.depth = depth

    def node_to_text(self, node: 'NodeType') -> 'Iterable[str]':
        stack = [iter(node)]
        while stack:
            try:
                item = next(stack[-1])
            except StopIteration:
                stack.pop()
                continue

            for item in self.process_node(item):
                if isinstance(item, str):
                    yield item
                else:
                    stack.append(iter(item))

    def process_node(self, node):
        if isinstance(node, DepthChange):
            self.depth = node.new_depth_for(self.depth)
        elif isinstance(node, Indentation):
            yield self.indentation * node.indents_for(self.depth)
        elif isinstance(node, Newline):
            yield self.newline
        else:
            yield node

    def dump(self, stream):
        for chunk in self.node_to_text(self.node):
            stream.write(chunk)

    def dumps(self):
        return ''.join(self.node_to_text(self.node))
