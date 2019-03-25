from .function_definition import Function


class Method(Function):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, 'self', *args, **kwargs)
