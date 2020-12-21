from .node import Node


class EmptyLines(Node):
    def __init__(self, count=1):
        super().__init__()
        self.count = count

    def header(self):
        for i in range(self.count):
            yield ''
