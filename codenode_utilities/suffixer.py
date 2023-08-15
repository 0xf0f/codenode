import codenode
from codenode import indentation, newline


def suffixer(
        suffix: str,
        dumps=lambda node: codenode.dumps(node),
):
    """
    Returns a node transformer that adds a string to the
    end of every line in the output of a node. Padding is added
    automatically to align all suffixes to the end of the longest line.

    :param suffix: String to place at the end of lines.
    :return: A function that takes a node as an argument,
             along with a function to convert a node to a string
             (i.e. codenode.dumps). It calls this function with
             the given node, then returns new nodes containing each
             line in the string along with the suffix at the end.
    """
    def suffixed(node):
        output_lines = dumps(node).splitlines()
        max_line_length = max(map(len, output_lines))
        for index, line_text in enumerate(output_lines):
            yield indentation
            yield line_text
            yield ' ' * (max_line_length - len(line_text))
            yield suffix
            yield newline

    return suffixed
