class DepthChange:
    def new_depth_for(self, depth: int) -> int:
        raise NotImplementedError


class RelativeDepthChange(DepthChange):
    def __init__(self, offset: int):
        self.offset = offset

    def new_depth_for(self, depth: int) -> int:
        return depth + self.offset

    def __repr__(self):
        return f'<RelativeDepthChange {self.offset:+}>'


class AbsoluteDepthChange(DepthChange):
    def __init__(self, value: int):
        self.value = value

    def new_depth_for(self, depth: int) -> int:
        return self.value

    def __repr__(self):
        return f'<AbsoluteDepthChange {self.value}>'

