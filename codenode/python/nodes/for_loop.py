from codenode.base import CodeNode
from .pass_statement import Pass


class For(CodeNode):
    def __init__(self, expression):
        super().__init__()

        self.expression = expression

    def header(self):
        yield f'for {self.expression}:'

    def body(self):
        if self.children:
            yield from self.children
        else:
            yield Pass()
