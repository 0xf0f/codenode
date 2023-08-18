import ast
import functools
import importlib
import inspect
import re
import textwrap
import types
import typing

import codenode_utilities
from codenode_utilities import prefixer

docstring_regex = re.compile(
    r'(?P<param>:param (?P<param_name>.+):(?P<param_description>[^:]*))|'
    r'(?P<return>:return[s]?:(?P<return_description>[^:]*))',
    re.MULTILINE,
)

signature_regex = re.compile(r'def .*(\(.*\).*?):', re.DOTALL | re.MULTILINE)


def dedent_lines(lines: str):
    return textwrap.dedent(lines)


def get_signature(function: types.FunctionType):
    source = inspect.getsource(function)
    node = ast.parse(textwrap.dedent(source))
    for child in ast.walk(node):
        if isinstance(child, ast.FunctionDef):
            result = f'({ast.unparse(child.args)})'
            if child.returns:
                result += f' -> {ast.unparse(child.returns)}'
            return result
    # for match in signature_regex.finditer(source):
    #     return ' '.join(
    #         map(
    #             str.strip,
    #             match.group(1).strip().rstrip(',')
    #             .splitlines()
    #         )
    #     )
    else:
        raise Exception(f'unable to find args for function {function.__name__}')

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
        'signature': f'def {function.__name__}{get_signature(function)}',
        **get_docstring_info(function.__doc__),
    }


def get_class_attributes_documentation(cls: typing.Type):
    if '__init__' in vars(cls):
        source = textwrap.dedent(inspect.getsource(cls.__init__))

        node = ast.parse(source)
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.FunctionDef):
                for a, b in zip(child.body, child.body[1:]):
                    if (
                        isinstance(b, ast.Expr) and
                        isinstance(b.value, ast.Constant) and
                        isinstance(b.value.value, str)
                    ):
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
                                'code': ast.unparse(a),
                            }
                elif isinstance(a, ast.AnnAssign):
                    if isinstance(a.target, ast.Name):
                        attribute_docs[a.target.id] = {
                            'description': b.value.value,
                            'type': ast.unparse(a.annotation),
                            'code': ast.unparse(a),
                        }
                else:
                    continue

        setattr(module, '__attribute_docs__', attribute_docs)
    return attribute_docs


def get_class_documentation(cls: typing.Type):
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




class DocumentationContent:
    def __init__(self, path: str, include_source_link=False):
        self.path = path
        self.include_source_link = include_source_link

    @functools.cache
    def get_module(self):
        module_path, _, attribute = self.path.rpartition('.')
        return importlib.import_module(module_path)

    @functools.cache
    def get_value(self):
        module_path, _, attribute = self.path.rpartition('.')
        module = importlib.import_module(module_path)
        return getattr(module, attribute)

    def get_documentation(self):
        yield line(f'### {self.path}<a id="{self.get_link()}"></a>')
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


from codenode import line, dumps, newline, lines, indent, dedent

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
        documentation = get_module_attribute_documentation(self.get_module()).get(name, '')
        if documentation:
            yield newline
            yield line('```python')
            yield line(documentation['code'])
            yield line('```')

            yield quote_block(line(documentation['description']))
            yield newline


functions = functools.partial(map, FunctionDocumentation)
classes = functools.partial(map, ClassDocumentation)
variables = functools.partial(map, AttributeDocumentation)
