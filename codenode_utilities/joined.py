# import itertools
from codenode import newline

sentinel = object()


def joined(nodes, *, start='', separator=newline, end=newline):
    """
    yields a starting node, then a sequence of nodes with a
    separator between each one, then an ending node

    :param nodes: sequence of nodes in the middle
    :param start: node at the start
    :param separator: node repeated between middle nodes
    :param end: ending node
    :return: iterable consisting of starting node, middle nodes with
             separators, and an ending node
    """
    # iterator = iter(nodes)
    #
    # yield start
    #
    # try:
    #     yield next(iterator)
    # except StopIteration:
    #     pass
    # else:
    #     yield from itertools.chain.from_iterable(
    #         zip(
    #             itertools.repeat(separator),
    #             iterator,
    #         )
    #     )
    #
    # yield end

    iterator = iter(nodes)
    item = next(iterator, sentinel)

    yield start

    while item is not sentinel:
        yield item
        item = next(iterator, sentinel)
        if item is not sentinel:
            yield separator
        else:
            yield end
