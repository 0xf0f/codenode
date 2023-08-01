import collections
import io
import typing

from .nodes.newline import Newline
from .nodes.indentation import Indentation
from .nodes.depth_change import DepthChange

if typing.TYPE_CHECKING:
    from typing import Union, Iterable
    NodeType = Iterable[Union[str, 'NodeType']]


class WriterStack:
    def __init__(self):
        self.items = collections.deque()

    def push(self, node: 'NodeType'):
        self.items.append(iter(node))

    def clear(self):
        self.items.clear()

    def __iter__(self) -> 'Iterable[NodeType]':
        while self.items:
            try:
                yield next(self.items[-1])
            except StopIteration:
                self.items.pop()


class Writer:
    def __init__(
            self,
            node: 'NodeType', *,
            indentation='    ',
            newline='\n',
            depth=0,
    ):
        self.node = node
        self.stack = WriterStack()

        self.indentation = indentation
        self.newline = newline
        self.depth = depth

    def process_node(self, node) -> 'Iterable[str]':
        """
        yield strings representing a node and/or apply any of its
        associated side effects to the writer

        for example:

        - yield indentation string when an indentation node is encountered

        - increase the current writer depth if an indent is encountered

        - append an iterator to the stack when an iterable is encountered

        :param node: node to be processed
        :returns: strings of text chunks representing the node
        """
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
                self.stack.push(node)
            except TypeError as error:
                raise TypeError(
                    f'Unable to process node "{node}".\n'
                    'Either convert it to a string, iterable or '
                    'override Writer.process_node to handle nodes '
                    'of this type.'
                ) from error

    def dump(self, stream):
        self.stack.clear()
        self.stack.push((self.node,))

        for node in self.stack:
            for chunk in self.process_node(node):
                stream.write(chunk)

    def dumps(self):
        buffer = io.StringIO()
        self.dump(buffer)
        return buffer.getvalue()
