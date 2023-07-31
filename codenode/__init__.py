from .writer import Writer
from .nodes.depth_change import RelativeDepthChange
from .nodes.indentation import CurrentIndentation
from .nodes.newline import Newline
from .debug import debug_patch

default_writer_type = Writer

indent = RelativeDepthChange(1)
dedent = RelativeDepthChange(-1)
indentation = CurrentIndentation()
newline = Newline()


def line(content):
    return indentation, content, newline


def lines(*items):
    return tuple(map(line, items))


def empty_lines(count: int):
    return (newline,) * count


def indented(*nodes):
    return indent, nodes, dedent


def dump(
        node, stream, *,
        indentation='    ',
        newline='\n',
        depth=0,
        debug=False,
):
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
):
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
    'dump', 'dumps'
]
