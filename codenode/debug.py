import copy
import io
import pprint
import typing

# from contextlib import contextmanager
from .writer import Writer


# class DebugNode:
#     pass


# @contextmanager
# def debug(writer: 'Writer'):
#     try:
#         yield writer
#     except Exception as e:
#         pass
#
#         self.debug = debug
#
#         if self.debug:
#             original_process_node = self.process_node
#
#             def debug_process_node(node):
#                 try:
#                     yield from original_process_node(node)
#                 except Exception as e:
#                     traceback = io.StringIO()
#                     traceback.write(''.join(map(str, e.args)))
#                     traceback.write('\n\nWriter stack:\n')
#                     for index, iterator in enumerate(self.stack[1:]):
#                         iterator: DebugIterator
#                         traceback.write(f'Node #{index}: ({iterator.items_yielded} items processed)\n')
#                         pprint.pprint(
#                             iterator.iterable,
#                             traceback,
#                             depth=1,
#                             compact=False,
#                             indent=2,
#                         )
#                         traceback.write('\n')
#                     traceback.write(f'Processing item: {iterator.current_item}')
#                     e.args = (traceback.getvalue(),)
#                     raise
#
#             self.process_node = debug_process_node


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


# class DebugStack(WriterStack):
#     def push(self, node):
#         self.append(DebugIterator(node))

def print_writer_stack(writer: Writer, stream):
    for index, iterator in enumerate(writer.stack[1:]):
        stream.write(f'Node #{index}: ')

        if isinstance(iterator, DebugIterator):
            stream.write(f'({iterator.items_yielded} items processed)\n')

            pprint.pprint(
                iterator.iterable,
                stream=stream,
                depth=1,
                compact=False,
                indent=2,
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

