class Indentation:
    def indents_for(self, depth: int) -> int:
        raise NotImplementedError


class RelativeIndentation(Indentation):
    def __init__(self, offset: int):
        self.offset = offset

    def indents_for(self, depth: int) -> int:
        return depth + self.offset


class AbsoluteIndentation(Indentation):
    def __init__(self, value: int):
        self.value = value

    def indents_for(self, depth: int) -> int:
        return self.value


class CurrentIndentation(Indentation):
    def indents_for(self, depth: int) -> int:
        return depth
