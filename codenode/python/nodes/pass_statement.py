from codenode.base import CodeNode


class Pass(CodeNode):
    def body(self):
        yield 'pass'
