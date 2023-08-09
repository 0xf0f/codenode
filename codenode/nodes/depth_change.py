class DepthChange:
    """
    Nodes that represent a change in indentation depth.
    """
    def new_depth_for(self, depth: int) -> int:
        """
        Method used to calculate the new depth based on the current one.

        :param depth: Current depth.
        :return: New depth.
        """
        raise NotImplementedError


class RelativeDepthChange(DepthChange):
    """
    Nodes that represent a change in indentation depth relative to the
    current depth by some preset amount.
    """
    def __init__(self, offset: int):
        """
        :param offset: Amount by which to increase/decrease depth.
        """
        self.offset = offset
        """
        Amount by which to increase/decrease depth when this node is
        processed.
        """

    def new_depth_for(self, depth: int) -> int:
        return depth + self.offset

    def __repr__(self):
        return f'<RelativeDepthChange {self.offset:+}>'


class AbsoluteDepthChange(DepthChange):
    """
    Nodes that represent a change in indentation depth without taking
    the current depth into account.
    """
    def __init__(self, value: int):
        """
        :param value: Value to set depth to.
        """
        self.value = value
        """
        Value to which depth will be set to when this node is
        processed.
        """

    def new_depth_for(self, depth: int) -> int:
        return self.value

    def __repr__(self):
        return f'<AbsoluteDepthChange {self.value}>'

