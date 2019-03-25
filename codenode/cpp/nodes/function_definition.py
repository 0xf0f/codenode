from codenode.base import CodeNode
from codenode.base import Block
from .block import Block as CppBlock


class Function(Block):
    def __init__(self, return_type, name, *args, **kwargs):
        super().__init__()

        self.return_type = return_type
        self.name = name
        self.args = args
        self.kwargs = kwargs

        self.block = CppBlock()
        self.children.append(self.block)

    def header(self):
        arg_string = ', '.join(self.args)
        if self.kwargs:
            if self.args:
                arg_string += ', '

            arg_string += ', '.join(
                f'{key}={value}' for key, value in self.kwargs.items()
            )

        yield f'{self.return_type} {self.name}({arg_string})'

    def add_child(self, child: 'CodeNode'):
        return self.block.add_child(child)
