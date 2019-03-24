from .codenode import CodeNode


class EmptyLines(CodeNode):
    def __init__(self, count=1):
        super().__init__()
        self.count = count

    def body(self):
        for i in range(self.count):
            yield ''
