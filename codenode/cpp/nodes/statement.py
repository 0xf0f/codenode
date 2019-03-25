from codenode.base import CodeNode


class Statement(CodeNode):
    def __init__(self, content):
        super().__init__()
        self.content = content

    def body(self):
        yield f'{self.content};'
