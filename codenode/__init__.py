from .writer import Writer
from .nodes.depth_change import RelativeDepthChange
from .nodes.indentation import CurrentIndentation
from .nodes.newline import Newline
from .debug import debug_patch

default_writer_type = Writer
"Default Writer type used in codenode.dump and codenode.dumps."

indent = RelativeDepthChange(1)
"A node representing a single increase in indentation level."

dedent = RelativeDepthChange(-1)
"A node representing a single decrease in indentation level."

indentation = CurrentIndentation()
"A placeholder node for indentation whitespace at the start of a line."

newline = Newline()
"A placeholder node for line terminators."


def line(content: 'T') -> 'tuple[Indentation, T, Newline]':
    """
    Convenience function that returns a tuple containing
    an indentation node, line content and a newline node.

    :param content: content of line
    :return: tuple containing an indentation node, line content and
             a newline node.
    """
    return indentation, content, newline


def lines(*items) -> tuple[tuple, ...]:
    """
    Convenience function that returns a tuple of lines,
    where each argument is the content of one line.

    :param items: contents of lines
    :return: tuple of lines
    """
    return tuple(map(line, items))


def empty_lines(count: int) -> 'tuple[Newline, ...]':
    """
    Convenience function that returns a tuple of newline nodes.

    :param count: Number of newlines.
    :return: Tuple of newlines.
    """
    return (newline,) * count


def indented(*nodes) -> tuple:
    """
    Convenience function that returns a tuple containing an indent node,
    some inner nodes, and a dedent node.

    :param nodes: inner nodes
    :return: tuple containing an indent node, inner nodes, and a dedent node.
    """
    return indent, nodes, dedent


def dump(
        node, stream, *,
        indentation='    ',
        newline='\n',
        depth=0,
        debug=False,
):
    """
    Process and write out a node tree to a stream.

    :param node: Base node of node tree.
    :param stream: An object with a 'write' method.
    :param indentation: String used for indents in the output.
    :param newline: String used for newlines in the output.
    :param depth: Base depth (i.e. number of indents) to start at.
    :param debug: If True, will print out extra info when an error
                  occurs to give a better idea of which node caused it.
    """
    if debug:
        writer_type = debug_patch(default_writer_type)
    else:
        writer_type = default_writer_type

    return writer_type(
        node,
        indentation=indentation,
        newline=newline,
        depth=depth,
    ).dump(stream)


def dumps(
        node, *,
        indentation='    ',
        newline='\n',
        depth=0,
        debug=False,
) -> str:
    """
    Process and write out a node tree as a string.

    :param node: Base node of node tree.
    :param indentation: String used for indents in the output.
    :param newline: String used for newlines in the output.
    :param depth: Base depth (i.e. number of indents) to start at.
    :param debug: If True, will print out extra info when an error
                  occurs to give a better idea of which node caused it.

    :return: String representation of node tree.
    """
    if debug:
        writer_type = debug_patch(default_writer_type)
    else:
        writer_type = default_writer_type

    return writer_type(
        node,
        indentation=indentation,
        newline=newline,
        depth=depth,
    ).dumps()


__all__ = [
    'indent', 'dedent', 'indented',
    'indentation', 'newline',
    'line', 'lines', 'empty_lines',
    'dump', 'dumps', 'default_writer_type',
]
