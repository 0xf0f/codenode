from codenode.base import CodeNode


class Block(CodeNode):
    def header(self):
        yield '{'

    def body(self):
        yield from self.children

    def footer(self):
        yield '}'
