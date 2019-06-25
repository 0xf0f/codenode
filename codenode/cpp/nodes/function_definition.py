from codenode.base import CodeNode


class Function(CodeNode):
    def __init__(self, return_type, name, *args, **kwargs):
        super().__init__()

        self.return_type = return_type
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def header(self):
        arg_string = ', '.join(self.args)
        if self.kwargs:
            if self.args:
                arg_string += ', '

            arg_string += ', '.join(
                f'{key}={value}' for key, value in self.kwargs.items()
            )

        yield f'{self.return_type} {self.name}({arg_string})'
        yield '{'

    def body(self):
        yield from self.children

    def footer(self):
        yield '}'
