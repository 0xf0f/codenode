from .node import Node


class Block(Node):
    child_depth_offset = 0

    def body(self):
        yield from self.children
