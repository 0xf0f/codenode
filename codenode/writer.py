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
    """
    A stack of iterators.
    Used by the Writer class to traverse node trees.

    Each instance is intended to be used once then discarded.
    """
    def __init__(self):
        self.items: collections.deque = collections.deque()
        """
        Current items in the stack.
        """

    def push(self, node: 'NodeType'):
        """
        Converts a node to an iterator then places it at
        the top of the stack.

        :param node: iterable node
        """
        self.items.append(iter(node))

    def __iter__(self) -> 'Iterable[NodeType]':
        """
        Continually iterates the top iterator in the stack's items,
        yielding each result then popping each iterator off when they
        are exhausted.
        """
        while self.items:
            try:
                yield next(self.items[-1])
            except StopIteration:
                self.items.pop()


class Writer:
    """
    Processes node trees into strings then writes out the result.

    Each instance is intended to be used once then discarded.
    After a single call to either dump or dumps, the Writer
    instance is no longer useful.
    """
    def __init__(
            self,
            node: 'NodeType', *,
            indentation='    ',
            newline='\n',
            depth=0,
    ):
        """
        :param node: Base node of node tree.
        :param indentation: Initial string used for indents in the output.
        :param newline: Initial string used for newlines in the output.
        :param depth: Base depth (i.e. number of indents) to start at.
        """
        self.node = node
        "Base node of node tree"

        self.stack = WriterStack()
        "WriterStack used to iterate over the node tree"
        self.stack.push((node,))

        self.indentation = indentation
        "Current string used for indents in the output"
        self.newline = newline
        "Current string used for line termination in the output"
        self.depth = depth
        "Current output depth (i.e. number of indents)"

    def process_node(self, node) -> 'Iterable[str]':
        """
        Yield strings representing a node and/or apply any of its
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
        """
        Process and write out a node tree to a stream.

        :param stream: An object with a 'write' method.
        """
        for node in self.stack:
            for chunk in self.process_node(node):
                stream.write(chunk)

    def dumps(self):
        """
        Process and write out a node tree as a string.

        :return: String representation of node tree.
        """
        buffer = io.StringIO()
        self.dump(buffer)
        return buffer.getvalue()
