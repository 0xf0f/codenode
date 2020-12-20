from codenode.base import CodeNode


class DocString(CodeNode):
    def __init__(self, content=''):
        super().__init__()
        self.content = content

    def header(self):
        yield '"""'

    def body(self):
        yield from self.content.splitlines()

    def footer(self):
        yield '"""'
