"""
This example demonstrates how to use codenode to generate some test placeholders.
The tests themselves require quicktest to run:
    https://github.com/0xf0f/quicktest
"""

import codenode as cn
import codenode.python as py

import inspect


def generate_class_tests(cls):
    test_list_name = f'{cls.__name__.lower()}_tests'

    file = cn.File()

    file.add_child(
        cn.Line('from quicktest import TestList')
    )

    file.add_child(
        py.Comment(f'import {cls.__name__} here')
    )

    file.add_child(cn.EmptyLines(2))

    file.add_child(
        cn.Line(
            f"{test_list_name} = TestList('{cls.__name__} tests')"
        )
    )
    file.add_child(cn.EmptyLines(2))

    for name, method in inspect.getmembers(
            cls, predicate=inspect.isroutine
    ):
        test_function = py.Function(f'test_{name}', 'instance')
        test_function.add_decorator(f'{test_list_name}.test')

        comment = py.Comment(test_function.dumps())

        file.add_child(comment)
        file.add_child(cn.EmptyLines(1))

    run_function = py.Function('run_tests')

    run_function.add_child(cn.Line(f'instance = {cls.__name__}()'))
    run_function.add_child(cn.Line(f'{test_list_name}.run(instance)'))

    file.add_child(run_function)

    return file


if __name__ == '__main__':
    class TestClass:
        def test_method(self):
            pass

    generated_tests = generate_class_tests(TestClass)

    # print results:
    print(generated_tests.dumps())

    # or to save to a file:
    with open('output.py', 'w') as file:
        generated_tests.dump(file)
