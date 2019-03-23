from base import CodeNode


class Function(CodeNode):
    def __init__(self, name, *args, **kwargs):
        super().__init__()
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def header(self):
        arg_string = ', '.join(self.args)
        if self.kwargs:
            if self.args:
                arg_string += ', '
            arg_string += ', '.join(
                map(lambda key, value: f'{key}={value}', self.kwargs.items())
            )

        yield f'def {self.name}({arg_string}):'

    def body(self):
        yield from self.children
