from typing import TypeVar, Union, Callable

HasStringWriteMethod = TypeVar('HasStringWriteMethod')
NodeArgumentType = Union['Node', str, list, tuple]
TransformerType = Callable[['Node'], 'Node']
