import typing

from .nodes.newline import Newline
from .nodes.indentation import Indentation
from .nodes.depth_change import DepthChange

if typing.TYPE_CHECKING:
    from typing import Union, Iterable, Iterator
    NodeType = Iterable[Union[str, 'NodeType']]


class Writer:
    def __init__(
            self,
            node: 'NodeType', *,
            indentation='    ',
            newline='\n',
            depth=0,
            auto_coerce=False,
    ):
        self.node = node
        self.stack: list['Iterator'] = list()

        self.indentation = indentation
        self.newline = newline
        self.depth = depth

        self.auto_coerce = auto_coerce

    def get_text_chunks(self) -> 'Iterable[str]':
        self.stack.clear()
        self.stack.append(iter((self.node,)))

        while self.stack:
            try:
                node = next(self.stack[-1])
            except StopIteration:
                self.stack.pop()
                continue

            yield from self.process_node(node)

    def process_node(self, node) -> 'Iterable[str]':
        if isinstance(node, str):
            yield node
        elif isinstance(node, DepthChange):
            self.depth = node.new_depth_for(self.depth)
        elif isinstance(node, Indentation):
            yield self.indentation * node.indents_for(self.depth)
        elif isinstance(node, Newline):
            yield self.newline
        else:
            try:
                self.stack.append(iter(node))
            except TypeError:
                if self.auto_coerce:
                    yield str(node)
                else:
                    raise TypeError(
                        f'Unable to process node "{node}".\n'
                        'Either convert it to a string, iterable or '
                        'override Writer.process_node to handle nodes '
                        'of this type.'
                    )

    def dump(self, stream):
        for chunk in self.get_text_chunks():
            stream.write(chunk)

    def dumps(self):
        return ''.join(self.get_text_chunks())
