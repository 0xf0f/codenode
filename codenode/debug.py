import io
import pprint
import typing

from .writer import Writer


class DebugIterator:
    def __init__(self, iterable):
        self.iterable = iterable
        self.iterator = iter(iterable)
        self.items_yielded = 0
        self.current_item = None

    def __iter__(self):
        return self

    def __next__(self):
        self.items_yielded += 1
        self.current_item = next(self.iterator)
        if not isinstance(self.current_item, str):
            try:
                self.current_item = DebugIterator(self.current_item)
            except TypeError:
                pass
        return self.current_item


def print_writer_stack(writer: Writer, stream):
    for index, iterator in enumerate(writer.stack[1:]):
        stream.write(f'Node #{index}: ')

        if isinstance(iterator, DebugIterator):
            stream.write(f'({iterator.items_yielded-1} items processed)\n')

            pprint.pprint(
                iterator.iterable,
                stream=stream,
                depth=2,
                compact=False,
                indent=2,
                width=128,
            )
        else:
            stream.write(repr(iterator))
            stream.write('\n')

        stream.write('\n')

    iterator = writer.stack[-1]
    if isinstance(iterator, DebugIterator):
        stream.write(f'Processing item: {iterator.current_item}')


def debug_patch(writer_type: typing.Type[Writer]):
    class PatchedWriter(writer_type):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.node = DebugIterator(self.node)

        def process_node(self, node) -> typing.Iterable[str]:
            try:
                yield from super().process_node(node)
            except Exception as e:
                buffer = io.StringIO()
                buffer.write(''.join(map(str, e.args)))
                buffer.write('\n\nWriter stack:\n')
                print_writer_stack(self, buffer)
                e.args = (buffer.getvalue(),)
                raise e

    return PatchedWriter


DebugWriter = debug_patch(Writer)
