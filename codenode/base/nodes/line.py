from .codenode import CodeNode


class Line(CodeNode):
    def __init__(self, content=''):
        super().__init__()

        self.content = content

    def body(self):
        yield self.content
