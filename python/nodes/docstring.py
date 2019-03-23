from base import CodeNode


class DocString(CodeNode):
    def __init__(self, content=''):
        super().__init__()
        self.content = content

    def header(self):
        yield '"""'

    def body(self):
        yield from self.content.split('\n')

    def footer(self):
        yield '"""'
