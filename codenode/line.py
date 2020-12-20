from .node import Node


class Line(Node):
    def __init__(self, content=''):
        super().__init__()

        self.content = content

    def header(self):
        yield self.content

