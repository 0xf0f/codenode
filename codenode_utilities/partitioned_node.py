from codenode import indent, dedent, dump, dumps

import typing

T = typing.TypeVar('T')


class PartitionedNode:
    """
    A node with three separate sections: a header, an indented body and
    a footer.

    Keeps track of child nodes using a list, which is yielded as the
    default body.

    Has convenience methods for adding children and dumping output using
    the default Writer type.
    """
    def __init__(self):
        self.children = []
        """
        Node in the body section.
        """

    def header(self) -> 'Iterable':
        """
        Starting section of node.
        """
        yield from ()

    def body(self) -> 'Iterable':
        """
        Middle section of node.
        Yields children by default.
        """
        yield from self.children

    def footer(self) -> 'Iterable':
        """
        Ending section of node.
        """
        yield from ()

    def __iter__(self):
        yield from self.header()
        yield indent
        yield from self.body()
        yield dedent
        yield from self.footer()

    def add_child(self, node: 'T') -> 'T':
        """
        Add a node to this node's children.

        :param node: Node to add.
        :return: Added node.
        """
        self.children.append(node)
        return node

    def add_children(self, nodes: typing.Iterable[T]) -> typing.Iterable[T]:
        """
        Add multiple nodes to this node's children.

        :param nodes: Nodes to add.
        :return: The added nodes
        """
        self.children.extend(nodes)
        return nodes

    def dump(
            self, stream, *,
            indentation='    ',
            newline='\n',
            depth=0,
            debug=False,
    ):
        """
        Process and write out this node to a stream.

        :param stream: An object with a 'write' method.
        :param indentation: String used for indents in the output.
        :param newline: String used for newlines in the output.
        :param depth: Base depth (i.e. number of indents) to start at.
        :param debug: If True, will print out extra info when an error
                      occurs to give a better idea of which node caused it.
        """
        return dump(
            self,
            stream,
            indentation=indentation,
            newline=newline,
            depth=depth,
            debug=debug,
        )

    def dumps(
            self, *,
            indentation='    ',
            newline='\n',
            depth=0,
            debug=False,
    ):
        """
        Process and write out this node as a string.

        :param indentation: String used for indents in the output.
        :param newline: String used for newlines in the output.
        :param depth: Base depth (i.e. number of indents) to start at.
        :param debug: If True, will print out extra info when an error
                      occurs to give a better idea of which node caused it.

        :return: String representation of node.
        """
        return dumps(
            self,
            indentation=indentation,
            newline=newline,
            depth=depth,
            debug=debug,
        )
