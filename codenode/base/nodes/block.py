from .codenode import CodeNode


class Block(CodeNode):
    child_depth_offset = 0

    def body(self):
        yield from self.children
