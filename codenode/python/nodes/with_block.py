from codenode.base import CodeNode
from .pass_statement import Pass


class With(CodeNode):
    def __init__(self, expression):
        super().__init__()

        self.expression = expression

    def header(self):
        yield f'with {self.expression}:'

    def body(self):
        if self.children:
            yield from self.children
        else:
            yield Pass()
