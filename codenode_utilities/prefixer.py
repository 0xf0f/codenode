import codenode
import io
import typing

# from .node_transformer import node_transformer
# from codenode.nodes.indentation import AbsoluteIndentation, CurrentIndentation
# from codenode.nodes.depth_change import RelativeDepthChange
#
#
# def prefixer(prefix):
#     """
#
#     :param prefix:
#     :return:
#     """
#     def prefixed(node):
#         indents = 0
#
#         @node_transformer
#         def transform(node):
#             nonlocal indents
#             if isinstance(node, RelativeDepthChange):
#                 indents += node.offset
#                 yield node
#             elif isinstance(node, CurrentIndentation):
#                 yield RelativeDepthChange(-indents)
#                 yield node
#                 yield prefix
#                 yield AbsoluteIndentation(indents)
#                 yield RelativeDepthChange(indents)
#             else:
#                 yield node
#
#         yield from transform(node)
#     return prefixed


# from .node_transformer import NodeTransformer
#
#
# def prefixer(prefix: str):
#     def prefixed(node):
#         indents = 0
#
#         class Prefixer(NodeTransformer):
#             def transform(self, node):
#                 nonlocal indents
#                 if isinstance(node, RelativeDepthChange):
#                     indents += node.offset
#                     yield node
#                 elif isinstance(node, CurrentIndentation):
#                     yield RelativeDepthChange(-indents)
#                     yield node
#                     yield prefix
#                     yield AbsoluteIndentation(indents)
#                     yield RelativeDepthChange(indents)
#                 else:
#                     yield node
#
#         return Prefixer(node)
#
#     return prefixed

# import inspect
#
# def get_writer_type():
#     stack = inspect.stack()
#     for frame_info in stack:
#         try:
#             cls = frame_info.frame.f_locals['__class__']
#         except KeyError:
#             continue
#         else:
#             if issubclass(cls, codenode.Writer):
#                 return cls
#
#
def yield_lines(iterator: typing.Iterable[str]):
    buffer = io.StringIO()
    for chunk in iterator:
        newline_position = chunk.find('\n')
        if newline_position >= 0:
            buffer.write(chunk[:newline_position])
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.write(chunk[newline_position+1:])
            buffer.truncate()
        else:
            buffer.write(chunk)
    if buffer.tell():
        yield buffer.getvalue()
#
#
# def prefixer(prefix: str):
#     def prefixed(
#             node,
#             dump_iter=None,
#     ):
#         if dump_iter is None:
#             writer_type = get_writer_type()
#             dump_iter = lambda node: writer_type(node).dump_iter()
#
#         for line_content in yield_lines(dump_iter(node)):
#             yield codenode.line(f'{prefix}{line_content}')
#     return prefixed


def prefixer(prefix: str):
    """
    Returns a node transformer that adds a string to the
    start of every line in the output of a node.

    :param prefix: String to place at the start of lines.
    :return: A function that takes a node as an argument,
             along with a function to convert a node to a string
             (i.e. codenode.dumps). It calls this function with
             the given node, then returns new nodes containing each
             line in the string along with the prefix at the start.
    """
    def prefixed(
            node,
            dumps=lambda node: codenode.dumps(node),
    ):
        for line_content in dumps(node).splitlines():
            yield codenode.line(f'{prefix}{line_content}')
    return prefixed


def prefixer_iter(prefix: str):
    """
    Returns a node transformer that adds a string to the
    start of every line in the output of a node. Works iteratively,
    line by line, rather than rendering out the node all at once.

    :param prefix: String to place at the start of lines.
    :return: A function that takes a node as an argument,
             along with a function to convert a node to an iterable of
             strings (i.e. codenode.Writer.dump_iter).
             It calls this function with the given node, then returns
             new nodes containing each line in the output along with the
             prefix at the start.
    """
    def prefixed(
            node,
            dump_iter=lambda node: codenode.default_writer_type(node).dump_iter()
    ):
        for line_content in yield_lines(dump_iter(node)):
            yield codenode.line(f'{prefix}{line_content}')
    return prefixed
