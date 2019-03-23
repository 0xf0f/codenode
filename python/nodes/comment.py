from base import CodeNode


class Comment(CodeNode):
    def __init__(self, content=''):
        super().__init__()
        self.content = content

    def body(self):
        for line in self.content.split('\n'):
            yield f'# {line}'
