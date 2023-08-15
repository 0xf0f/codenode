import typing
from codenode.writer import Writer

T = typing.TypeVar('T', bound=typing.Type[Writer])


def auto_coerce_patch(
        writer_type: T,
        coerce=str,
) -> T:
    """
    Returns an altered version of a writer type
    that will automatically convert unprocessable nodes to
    another type.

    :param writer_type: Base writer type.
    :param coerce: Callable used to convert nodes. str by default.
    :return: Descendant writer type that will convert unprocessable nodes.
    """
    class PatchedWriter(writer_type):
        def process_node(self, node):
            try:
                yield from super().process_node(node)
            except TypeError:
                yield coerce(node)

    return PatchedWriter
