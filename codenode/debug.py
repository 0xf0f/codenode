import collections
import functools
import io
import pprint
import types
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

    for index, iterator in enumerate(writer.stack):
        stream.write(f'Node #{index}: ')

        if isinstance(iterator, DebugIterator):
            stream.write(f'({iterator.items_yielded-1} items processed)\n')

            if isinstance(iterator.iterable, typing.Sequence):
                for sub_index, sub_item in enumerate(iterator.iterable):
                    stream.write(f'item {sub_index}: ')
                    pretty_print(sub_item)

            else:
                pretty_print(iterator.iterable)

                stream.write(f'Last {len(iterator.item_buffer)} items processed: \n')
                for item in iterator.item_buffer:
                    pretty_print(item)
        else:
            stream.write(repr(iterator))
            stream.write('\n')

        stream.write('\n')

    iterator = writer.stack[-1]
    if isinstance(iterator, DebugIterator):
        stream.write(f'Last {len(iterator.item_buffer)} items processed: \n')
        for item in iterator.item_buffer:
            pretty_print(item)


def mask_globals(masked_globals: dict):
    def patch(function: types.FunctionType):
        return types.FunctionType(
            code=function.__code__,
            globals={**function.__globals__, **masked_globals},
            name=function.__name__,
            argdefs=function.__defaults__,
            closure=function.__closure__,
        )
    return patch


def debug_patch(writer_type: typing.Type[Writer]):
    patch_iter = mask_globals({'iter': DebugIterator})

    class PatchedWriter(writer_type):
        def patched_process_node(self, node) -> typing.Iterable[str]:
            raise NotImplementedError

        def process_node(self, node) -> typing.Iterable[str]:
            try:
                yield from self.patched_process_node(node)
            except Exception as e:
                buffer = io.StringIO()
                buffer.write(''.join(map(str, e.args)))
                buffer.write('\n\nWriter stack:\n')
                print_writer_stack(self, buffer)
                e.args = (buffer.getvalue(),)
                raise

    PatchedWriter.dump = patch_iter(writer_type.dump)
    PatchedWriter.patched_process_node = patch_iter(writer_type.process_node)

    return PatchedWriter
