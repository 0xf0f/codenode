class Indentation:
    """
    Nodes that represent indentation whitespace at the start of a line.
    """
    def indents_for(self, depth: int) -> int:
        """
        :param depth: Current depth.
        :return: Number of indents to include in whitespace when this
        node is processed.
        """
        raise NotImplementedError


class RelativeIndentation(Indentation):
    """
    Nodes that represent indentation whitespace at the start of a line,
    with a number of indents relative to the current depth by some
    preset amount.
    """
    def __init__(self, offset: int):
        """
        :param offset: Amount of indents relative to the current depth.
        """
        self.offset = offset
        """
        Amount of indents relative to the current depth that will be
        output when this node is processed.
        """

    def indents_for(self, depth: int) -> int:
        return depth + self.offset

    def __repr__(self):
        return f'<RelativeIndentation {self.offset:+}>'


class AbsoluteIndentation(Indentation):
    """
    Nodes that represent indentation whitespace at the start of a line,
    with a number of indents independent of the current depth.
    """
    def __init__(self, value: int):
        """
        :param value: Amount of indents.
        """
        self.value = value
        """
        Amount of indents that will be output when this node is processed.
        """

    def indents_for(self, depth: int) -> int:
        return self.value

    def __repr__(self):
        return f'<AbsoluteIndentation {self.value}>'


class CurrentIndentation(Indentation):
    """
    Nodes that represent indentation whitespace at the start of a line,
    with a number of indents equal to the current depth.
    """
    def indents_for(self, depth: int) -> int:
        return depth

    def __repr__(self):
        return f'<Indentation>'
