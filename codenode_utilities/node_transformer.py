import functools


def node_transformer(func):
    """
    decorator for creating functions that are used to
    recursively transform node trees.

    :param func: transformer function applied to each node
    :return: a function which recursively applies the transformer
             function to each node in the tree.
    """
    @functools.wraps(func)
    def wrapper(node):
        if isinstance(node, str):
            yield func(node)
        else:
            try:
                yield from map(wrapper, node)
            except TypeError:
                yield func(node)
    return wrapper


# class NodeTransformer:
#     """
#     has a repr for extra debug info
#     """
#
#     def __init__(self, node):
#         self.node = node
#
#     def transform(self, node):
#         raise NotImplementedError
#
#     def __iter__(self):
#         if isinstance(self.node, str):
#             yield self.transform(self.node)
#         else:
#             try:
#                 yield from map(type(self), self.node)
#             except TypeError:
#                 yield self.transform(self.node)
#
#     def __repr__(self):
#         return f'{super().__repr__()}({self.node})'
#
