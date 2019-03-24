from codenode.base import CodeNode
from .pass_statement import Pass


class Class(CodeNode):
    def __init__(self, name, *parents):
        super().__init__()

        self.name = name
        self.parents = parents

    def header(self):
        if self.parents:
            yield f"class {self.name}({', '.join(self.parents)}):"
        else:
            yield f'class {self.name}:'

    def body(self):
        if self.children:
            yield from self.children
        else:
            yield Pass()
