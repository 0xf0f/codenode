### Contents
- [What is this?](#what-is-this)
- [How do I install it?](#how-do-i-install-it)
- [How do I use it?](#how-do-i-use-it)
- [Extensions](#extensions)
- [Reference](#reference)

### What is this?<a id="what-is-this"></a>
The goal of this module is to help write code that generates code. 
Focus is placed on enabling the user to easily describe, 
build and reason about code structures rapidly.

### How do I install it?<a id="how-do-i-install-it"></a>

[comment]: <> (### From PyPI:)

[comment]: <> (`pip install 0xf0f-codenode`)

#### From GitHub:
`pip install git+https://github.com/0xf0f/codenode`

### How do I use it?<a id="how-do-i-use-it"></a>
Like the `json` and 
`pickle` modules, `dump` and `dumps` are used to generate output. 
Code can be built using any tree of iterables containing strings, 
indentation nodes and newline nodes.

For example, the built-in `line` function returns a tuple:

```python
from codenode import indentation, newline

def line(content):
    return indentation, content, newline
```

Which we can combine with `indent` and `dedent` nodes:

```python
from codenode import line, indent, dedent, dumps

def counting_function(count_from, count_to):
    return [
        line(f'def count_from_{count_from}_to_{count_to}():'),
        indent,
        [
            line(f'print({i})')
            for i in range(count_from, count_to)
        ],
        dedent,
    ]

print(dumps(counting_function(0, 5)))
```

Which outputs:
```
def count_from_0_to_5():
    print(0)
    print(1)
    print(2)
    print(3)
    print(4)
```

But what if we want to count to a really big number, like 
1,000,000,000,000,000?
It would be inefficient to store all those lines in memory
at once. We can use a generator to break them down into 
individual parts instead:

```python
from codenode import indent, dedent, newline, indentation, dump

def counting_function_generator(count_from, count_to):
    yield indentation 
    yield 'def count_from_', str(count_from), '_to_', str(count_to), '():'
    yield newline
    
    yield indent
    for i in range(count_from, count_to):
        yield indentation, 'print(', str(i), ')', newline
    yield dedent

with open('code.py', 'w') as file:
    dump(counting_function_generator(0, 1_000_000_000_000_000), file)
```

We can also build a class with an `__iter__` method:

```python
from codenode import line, indent, dedent, dump

class CountingFunction:
    def __init__(self, count_from, count_to):
        self.count_from = count_from
        self.count_to = count_to
    
    def __iter__(self):
        yield line(
            f'def count_from_{self.count_from}_to_{self.count_to}():'
        )
        yield indent
        for i in range(self.count_from, self.count_to):
            yield line(f'print({i})')
        yield dedent

with open('code.py', 'w') as file:
    dump(CountingFunction(0, 1_000_000), file)
```

Or a more generalized function class:

```python
class Function:
    def __init__(self, name, *args):
        self.name = name
        self.args = args
        self.children = []
    
    def __iter__(self):
        arg_string = ', '.join(self.args)
        yield line(f'def {self.name}({arg_string}):')
        yield indent
        yield self.children
        yield dedent

class CountingFunction(Function):
    def __init__(self, count_from, count_to):
        super().__init__(f'count_from_{count_from}_to_{count_to}')
        for i in range(count_from, count_to):
            self.children.append(line(f'print({i})'))
```

Leveraging python's iteration protocol like this allows:
- Mixing and matching whatever fits the use case to maximize tradeoffs, 
such as using generators for their memory efficiency, 
custom iterable classes for their semantics, or plain old lists and 
tuples for their simplicity.
- Taking advantage of existing modules that offer tooling for 
iterables, such as itertools.
- Building higher level structures from as many iterable building blocks
as desired.

### Extensions<a id="extensions"></a>
Module behaviour can be extended by overriding methods of the 
`codenode.writer.Writer` and `codenode.writer.WriterStack` classes. An
example of this can be seen in the `codenode.debug.debug_patch` 
function. The variable `codenode.default_writer_type` can be used to
replace the `Writer` type used in `dump` and `dumps` with a custom one.

Some modules with helper classes and functions are also provided:
  - [codenode_utilities](codenode_utilities/README.md)
    - contains general language agnostic helper functions and classes

[comment]: <> (  - codenode_python)

[comment]: <> (    - contains helper classes and functions for generating python code)

[comment]: <> (  - codenode_cpp)

[comment]: <> (    - contains helper classes and functions for generating c++ code)

[comment]: <> (  - codenode_legacy)

[comment]: <> (    - helpers for code that relies on the old codenode API &#40;below version 1.0&#41;)

[comment]: <> (    - uses a previous, entirely different approach to nodes)

### Reference<a id="reference"></a>
> **Note**
> This section of the readme was generated using codenode itself.
> 
> See docs/generate_readme.py

#### Contents
${reference_contents}

${reference}
