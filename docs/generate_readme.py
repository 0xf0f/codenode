import ast
import importlib
import inspect
import functools
import re
import textwrap
import types
import typing

from codenode import line, dumps, dump
from codenode_utilities import prefixer

docstring_regex = re.compile(
    r'(?P<param>:param (?P<param_name>.+): (?P<param_description>[^:]+))|'
    r'(?P<return>:return[s]?: (?P<return_description>[^:]+))',
    re.MULTILINE,
)

# class_attributes_regex = re.compile(
#     r"self\.(?P<name>\S+)\s*(\s*:\s+(?P<type>.*?)\s+)?=.*?"
#     r"(?P<quote>[\"']{3}|[\"'])(?P<description>.*?)(?P=quote)",
#     re.MULTILINE | re.DOTALL,
# )


def dedent_lines(lines: str):
    return textwrap.dedent(lines)


def get_docstring_info(docstring):
    result = {
        'summary': '',
        'params': [],
        'return': '',
    }

    matches = (*docstring_regex.finditer(docstring),)

    for match in matches:
        result['summary'] = dedent_lines(docstring[:match.start()])
        break
    else:
        result['summary'] = dedent_lines(docstring)

    for match in matches:
        groups = match.groupdict()
        if groups.get('param', ''):
            result['params'].append(
                {
                    'name': groups['param_name'],
                    'description': dedent_lines(groups['param_description']),
                }
            )
        if groups.get('return', ''):
            result['return'] = dedent_lines(groups['return_description'])
    return result


def get_function_documentation(function: types.FunctionType):
    return {
        'name': function.__name__,
        'signature': f'def {function.__name__}{inspect.signature(function)}',
        **get_docstring_info(function.__doc__),
    }


def get_class_attributes_documentation(cls: typing.Type):
    if '__init__' in vars(cls):
        # print('attributes', cls)
        source = textwrap.dedent(inspect.getsource(cls.__init__))

        # return [
        #     {
        #         'name': match.group('name'),
        #         'description': match.group('description'),
        #         'type': match.group('type')
        #     }
        #     for match in class_attributes_regex.finditer(source)
        # ]

        node = ast.parse(source)
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.FunctionDef):
                for a, b in zip(child.body, child.body[1:]):
                    if (
                        isinstance(b, ast.Expr) and
                        isinstance(b.value, ast.Constant) and
                        isinstance(b.value.value, str)
                    ):
                        print(a, b)
                        if isinstance(a, ast.Assign):
                            for target in a.targets:
                                if (
                                    isinstance(target, ast.Attribute) and
                                    isinstance(target.value, ast.Name) and
                                    target.value.id == 'self'
                                ):
                                    yield {
                                        'name': target.attr,
                                        'description': dedent_lines(b.value.value.strip()),
                                        'type': '',
                                    }
                        elif isinstance(a, ast.AnnAssign):
                            if (
                                    isinstance(a.target, ast.Attribute) and
                                    isinstance(a.target.value, ast.Name) and
                                    a.target.value.id == 'self'
                            ):
                                yield {
                                    'name': a.target.attr,
                                    'description': dedent_lines(b.value.value.strip()),
                                    'type': ast.unparse(a.annotation)
                                }


def get_module_attribute_documentation(module: types.ModuleType):
    try:
        attribute_docs = getattr(module, '__attribute_docs__')
    except AttributeError:
        source = inspect.getsource(module)
        node = ast.parse(source)
        attribute_docs = dict()

        for a, b in zip(node.body, node.body[1:]):
            if (
                    isinstance(b, ast.Expr) and
                    isinstance(b.value, ast.Constant) and
                    isinstance(b.value.value, str)
            ):
                if isinstance(a, ast.Assign):
                    for target in a.targets:
                        if isinstance(target, ast.Name):
                            attribute_docs[target.id] = {
                                'description': b.value.value,
                                'type': '',
                            }
                elif isinstance(a, ast.AnnAssign):
                    if isinstance(a.target, ast.Name):
                        attribute_docs[a.target.id] = {
                            'description': b.value.value,
                            'type': ast.unparse(a.annotation),
                        }
        setattr(module, '__attribute_docs__', attribute_docs)
    return attribute_docs


def get_class_documentation(cls: typing.Type):
    print(cls)
    return {
        'name': cls.__name__,
        'summary': dedent_lines(cls.__doc__ or ''),
        'methods': [
            get_function_documentation(member)
            for member in vars(cls).values()
            if isinstance(member, types.FunctionType)
            and member.__doc__
        ],
        'attributes': tuple(get_class_attributes_documentation(cls)),
    }


from codenode import dumps, dump, Writer
print(get_class_documentation(Writer))


# class ModuleDocumentation:
#     pass
#
#

class DocumentationContent:
    def __init__(self, path: str):
        self.path = path

    # def get_source_link(self):
    #     obj = self.get_value()
    #     lines = inspect.getsourcelines(obj)
    #     file = inspect.getsourcefile(obj)
    #     return '[View Source]()'

    @functools.cache
    def get_module(self):
        module_path, _, attribute = self.path.rpartition('.')
        return importlib.import_module(module_path)

    @functools.cache
    def get_value(self):
        module_path, _, attribute = self.path.rpartition('.')
        module = importlib.import_module(module_path)
        print(module_path, attribute)
        return getattr(module, attribute)

    def get_documentation(self):
        yield line(f'### {self.path}')
        yield newline
        # yield line('---')

    @functools.cache
    def get_link(self):
        return '-'.join(
            re.sub(
                r'\s+', '-',
                self.path.lower().translate(str.maketrans({'.': None}))
            ).strip().split()
        )

    def __iter__(self):
        return self.get_documentation()

    def __repr__(self):
        return f'<Documentation {self.path}>'


from codenode import line, dumps, newline, lines, indent, dedent, indentation

quote_block = prefixer('> ')


def function_param_docs(params: dict):
    for param in params:
        yield line(''.join((
            f'* > ***{param["name"]}',
            # f' ({param["type"]})' if param["type"] else "",
            f':*** ',
        )))
        yield (
            line(f'  > {line_content}')
            for line_content in param["description"].splitlines()
        )


class ClassDocumentation(DocumentationContent):
    def get_documentation(self):
        yield from super().get_documentation()

        cls = self.get_value()
        documentation = get_class_documentation(cls)
        yield quote_block((
            line('```python'),
            line(f'class {cls.__name__}: ...'),
            line('```'),
            (
                line(f'{line_content}')
                for line_content in documentation['summary'].splitlines()
            ),
        ))

        if documentation['methods']:
            yield line('#### Methods')
            for method in documentation['methods']:
                yield quote_block((
                    line(f'##### `{method["name"]}`'),
                    # line('#### Summary'),
                    tuple((
                        line('```python'),
                        line(f'class {cls.__name__}:'),
                        indent,
                        line(f'{method["signature"]}: ...'),
                        dedent,
                        line('````'),
                        lines(*method['summary'].splitlines()),
                    )),
                    line(''),
                    (
                        line('#### Parameters'),
                        *function_param_docs(method['params']),
                    ) if method['params'] else (),
                    (
                        line('#### Returns'),
                        line(f'* > {method["return"]}'),
                    ) if method["return"] else (),
                ))
                yield newline

        if documentation['attributes']:
            yield line('#### Attributes')

            for attribute in documentation['attributes']:
                yield quote_block((
                    line(
                        f'***{attribute["name"]}:*** ' +
                        (f'{attribute["type"]} - ' if attribute["type"] else "")
                    ),
                    *(
                        line(f'{line_content}')
                        for line_content in attribute["description"].splitlines()
                    ),
                ))
                yield newline


class FunctionDocumentation(DocumentationContent):
    def get_documentation(self):
        yield from super().get_documentation()

        function = self.get_value()
        documentation = get_function_documentation(function)

        yield quote_block((
            # line('#### Summary'),
            tuple((
                line('```python'),
                line(f'{documentation["signature"]}: ...'),
                line('````'),
                lines(*documentation['summary'].splitlines()),
            )),
            line(''),
            (
                line('#### Parameters'),
                *function_param_docs(documentation['params']),
            ) if documentation['params'] else (),
            (
                line('#### Returns'),
                line(f'* > {documentation["return"]}'),
            ) if documentation["return"] else (),
        ))
        yield newline


class AttributeDocumentation(DocumentationContent):
    def get_documentation(self):
        yield from super().get_documentation()
        module, _, name = self.path.rpartition('.')
        docstring = get_module_attribute_documentation(self.get_module()).get(name, '')
        if docstring:
            yield newline
            yield quote_block(line(docstring['description']))
            yield newline

import functools

functions = functools.partial(map, FunctionDocumentation)
classes = functools.partial(map, ClassDocumentation)
variables = functools.partial(map, AttributeDocumentation)


contents = (
    *functions(
        (
            'codenode.dump',
            'codenode.dumps',
            'codenode.line',
        )
    ),

    *variables(
        (
            'codenode.indent',
            'codenode.dedent',
            'codenode.newline',
            'codenode.indentation',
        )
    ),

    *functions(
        (
            'codenode.lines',
            'codenode.empty_lines',
            'codenode.indented',
        )
    ),

    AttributeDocumentation('codenode.default_writer_type'),

    *classes(
        (
            'codenode.writer.Writer',
            'codenode.writer.WriterStack',

            'codenode.nodes.newline.Newline',

            'codenode.nodes.depth_change.DepthChange',
            'codenode.nodes.depth_change.RelativeDepthChange',
            'codenode.nodes.depth_change.AbsoluteDepthChange',

            'codenode.nodes.indentation.Indentation',
            'codenode.nodes.indentation.RelativeIndentation',
            'codenode.nodes.indentation.AbsoluteIndentation',
            'codenode.nodes.indentation.CurrentIndentation',

            # 'codenode.debug.DebugIterator',
        )
    ),

    *functions(
        (
            # 'codenode.debug.print_writer_stack',
            'codenode.debug.debug_patch',
        )
    ),
)


def reference_contents():
    for item in contents:
        yield line(f'- [{item.path}](#{item.get_link()})')


def reference():
    for item in contents:
        yield line('---')
        yield item

import string
import pathlib

if __name__ == '__main__':
    # print(parse(dumps.__doc__).returns.description)
    cd = pathlib.Path(__file__).absolute().parent
    with open(cd / 'readme_template.md') as file:
        template = string.Template(file.read())

    with open(cd.parent / 'README.md', 'w') as file:
        file.write(
            template.safe_substitute(
                {
                    'reference_contents': dumps(reference_contents(), debug=True),
                    'reference': dumps(reference(), debug=True),
                }
            )
        )
