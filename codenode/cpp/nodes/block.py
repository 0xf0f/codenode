from codenode.base import CodeNode


class Block(CodeNode):
    def header(self):
        yield '{'

    def footer(self):
        yield '}'
