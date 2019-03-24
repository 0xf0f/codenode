from base import CodeNode
from .pass_statement import Pass


class While(CodeNode):
    def __init__(self, condition):
        super().__init__()

        self.condition = condition

    def header(self):
        yield f'for {self.condition}:'

    def body(self):
        if self.children:
            yield from self.children
        else:
            yield Pass()
