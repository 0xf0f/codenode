from base import CodeNode


class Call(CodeNode):
    def __init__(self, name, *args, **kwargs):
        super().__init__()

        self.name = name
        self.args = args
        self.kwargs = kwargs

    def body(self):
        arg_string = ', '.join(self.args)
        if self.kwargs:
            if self.args:
                arg_string += ', '

            arg_string += ', '.join(
                f'{key}={value}' for key, value in self.kwargs.items()
            )

        yield f'{self.name}({arg_string})'
