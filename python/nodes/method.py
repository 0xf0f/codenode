from .function_definition import Function


class Method(Function):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, 'self')

        self.args.extend(args)
        self.kwargs.update(kwargs)
