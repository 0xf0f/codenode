import textwrap
import codenode

code = """
def test():
    print(0)
    print(1)
    print(2)
    print(3)
""".lstrip()


def basic_test():
    from codenode import (
        line,
        indent, dedent,
        indentation, newline,
        dumps,
    )

    node = [
        line('def test():'),
        indent,
        [
            line(f'print({i})')
            for i in range(4)
        ],
        dedent,
    ]

    assert dumps(node) == code

    altered_code = textwrap.indent(code, prefix='  ')
    altered_code = altered_code.replace('\n', '+').replace('    ', ' ')
    assert dumps(node, newline='+', indentation=' ', depth=2) == altered_code

    def generator():
        yield indentation
        yield 'def test():'
        yield newline
        yield indent
        for i in range(4):
            yield indentation
            yield 'print('
            yield str(i)
            yield ')'
            yield newline
        yield dedent

    assert codenode.dumps(generator()) == code


if __name__ == '__main__':
    basic_test()

