from .writer import Writer
from .nodes.depth_change import RelativeDepthChange
from .nodes.indentation import CurrentIndentation
from .nodes.newline import Newline


indent = RelativeDepthChange(1)
dedent = RelativeDepthChange(-1)
indentation = CurrentIndentation()
newline = Newline()


def line(content: str):
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
):
    return Writer(
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
):
    return Writer(
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
