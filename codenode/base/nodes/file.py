from .block import Block


class File(Block):
    def save(self, path, indent=None, base_depth=0):
        with open(path, 'w') as file:
            self.dump(file, indent, base_depth)
