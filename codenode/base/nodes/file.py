from .block import Block
from codenode.functionality.constants import default_indent


class File(Block):
    def save(self, path, indent=default_indent, base_depth=0):
        with open(path, 'w') as file:
            self.dump(file, indent, base_depth)
