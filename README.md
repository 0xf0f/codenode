### What is this?

The goal of this module is to help write code that generates code. 
Focus is placed on enabling the user to easily describe, 
build and reason about code structures rapidly.

### How do I install it?

[comment]: <> (### From PyPI:)

[comment]: <> (`pip install 0xf0f-codenode`)

#### From GitHub:
`pip install git+https://github.com/0xf0f/codenode`

### How do I use it?
Code can be built using any tree of iterables containing strings, 
indentation nodes and newline nodes. Like the `json` and `pickle` 
modules, `dump` and `dumps` are used to generate output.

Here's a simple example:

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

# line is a convenience function that returns a tuple containing:
# - an indentation node
#       (placeholder for configurable indentation characters)
# - line content
# - and a newline node 
#       (placeholder for configurable newline characters)

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

Leveraging python's iteration protocol like this allows:
- Mixing and matching whatever fits the use case to maximize tradeoffs, 
such as using generators for their memory efficiency, 
custom iterable classes for their semantics, or plain old lists and 
tuples for their simplicity.
- Taking advantage of existing modules that offer tooling for 
iterables, such as itertools.
- Building higher level structures from as many iterable building blocks
as desired.

Carrying on from the previous example, what if we want to count to an 
extremely high number, like 1,000,000?
It would be inefficient to store all the lines in memory
at once. We can use a generator to break them down into individual parts 
instead:

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
    dump(counting_function_generator(0, 1_000_000), file)
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

Or build a more generalized function class:
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
### Extensions
Module behaviour can be extended by overriding methods of the 
`codenode.writer.Writer` and `codenode.writer.WriterStack` classes. An
example of this can be seen in the `codenode.debug.debug_patch` 
function. The variable `codenode.default_writer_type` can be used to
replace the `Writer` type used in `dump` and `dumps` with a custom one.

Some modules with helper classes and functions are also provided:
  - codenode_utilities
    - contains general language agnostic helper functions and classes
  - codenode_python
    - contains helper classes and functions for generating python code
  - codenode_cpp
    - contains helper classes and functions for generating c++ code
  - codenode_legacy
    - helpers for code that relies on the old codenode API (below version 1.0)
    - uses a previous, entirely different approach to nodes

${reference}
