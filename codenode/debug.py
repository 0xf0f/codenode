import collections
import functools
import io
import pprint
import typing

from .writer import Writer


class DebugIterator:
    def __init__(self, iterable):
        self.iterable = iterable
        self.iterator = iter(iterable)
        self.items_yielded = 0
        self.item_buffer = collections.deque(maxlen=8)

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self.iterator)
        self.items_yielded += 1
        self.item_buffer.append(item)
        return item

    @property
    def current_item(self):
        return self.item_buffer[-1] if len(self.item_buffer) else None


def print_writer_stack(writer: Writer, stream):
    pretty_print = functools.partial(
        pprint.pprint,
        stream=stream,
        depth=2,
        compact=False,
        indent=2,
        width=128,
    )

    for index, iterator in enumerate(writer.stack.items):
        stream.write(f'node #{index}: \n')
        stream.write(f'type: {type(iterator.iterable)}\n')
        if isinstance(iterator, DebugIterator):
            if isinstance(iterator.iterable, typing.Sequence):
                for sub_index, sub_item in enumerate(iterator.iterable):
                    stream.write(f'  item {sub_index}: ')
                    pretty_print(sub_item)

            else:
                pretty_print(iterator.iterable)
            stream.write(
                f'  last {len(iterator.item_buffer)} items processed: '
                f'({iterator.items_yielded} total items processed)\n'
            )
            for item in iterator.item_buffer:
                stream.write('    ')
                pretty_print(item)
        else:
            stream.write(repr(iterator))
            stream.write('\n')

        stream.write('\n')


def debug_patch(writer_type: typing.Type[Writer]):
    class PatchedWriter(writer_type):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            push = self.stack.push
            self.stack.push = lambda node: push(DebugIterator(node))

        def dump(self, stream):
            try:
                return super().dump(stream)
            except Exception as e:
                buffer = io.StringIO()
                buffer.write(''.join(map(str, e.args)))
                buffer.write('\n\nWriter stack:\n')
                print_writer_stack(self, buffer)
                e.args = (buffer.getvalue(),)
                raise

    return PatchedWriter
