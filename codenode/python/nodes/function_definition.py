from codenode.base import CodeNode
from .pass_statement import Pass


class Function(CodeNode):
    def __init__(self, name, *args, **kwargs):
        super().__init__()
        self.name = name
        self.args = args
        self.kwargs = kwargs

        self.decorators = []

    def add_decorator(self, decorator):
        self.decorators.append(decorator)

    def header(self):
        for decorator in self.decorators:
            yield f'@{decorator}'

        arg_string = ', '.join(self.args)
        if self.kwargs:
            if self.args:
                arg_string += ', '

            arg_string += ', '.join(
                f'{key}={value}' for key, value in self.kwargs.items()
            )

        yield f'def {self.name}({arg_string}):'

    def body(self):
        if self.children:
            yield from self.children

        else:
            yield Pass()

