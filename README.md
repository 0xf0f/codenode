### Contents
- [What is this?](#what-is-this)
- [How do I install it?](#how-do-i-install-it)
- [How do I use it?](#how-do-i-use-it)
- [Extensions](#extensions)
- [Reference](#reference)

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

[comment]: <> (  - codenode_cpp)

[comment]: <> (    - contains helper classes and functions for generating c++ code)

[comment]: <> (  - codenode_legacy)

[comment]: <> (    - helpers for code that relies on the old codenode API &#40;below version 1.0&#41;)

[comment]: <> (    - uses a previous, entirely different approach to nodes)

### Reference
> **Note**
> This section of the readme was generated using codenode itself.
> 
> See docs/generate_readme.py

#### Contents
- [codenode.dump](#codenodedump)
- [codenode.dumps](#codenodedumps)
- [codenode.line](#codenodeline)
- [codenode.indent](#codenodeindent)
- [codenode.dedent](#codenodededent)
- [codenode.newline](#codenodenewline)
- [codenode.indentation](#codenodeindentation)
- [codenode.lines](#codenodelines)
- [codenode.empty_lines](#codenodeempty_lines)
- [codenode.indented](#codenodeindented)
- [codenode.default_writer_type](#codenodedefault_writer_type)
- [codenode.writer.Writer](#codenodewriterwriter)
- [codenode.writer.WriterStack](#codenodewriterwriterstack)
- [codenode.nodes.newline.Newline](#codenodenodesnewlinenewline)
- [codenode.nodes.depth_change.DepthChange](#codenodenodesdepth_changedepthchange)
- [codenode.nodes.depth_change.RelativeDepthChange](#codenodenodesdepth_changerelativedepthchange)
- [codenode.nodes.depth_change.AbsoluteDepthChange](#codenodenodesdepth_changeabsolutedepthchange)
- [codenode.nodes.indentation.Indentation](#codenodenodesindentationindentation)
- [codenode.nodes.indentation.RelativeIndentation](#codenodenodesindentationrelativeindentation)
- [codenode.nodes.indentation.AbsoluteIndentation](#codenodenodesindentationabsoluteindentation)
- [codenode.nodes.indentation.CurrentIndentation](#codenodenodesindentationcurrentindentation)
- [codenode.debug.debug_patch](#codenodedebugdebug_patch)


---
### codenode.dump

> ```python
> def dump(node, stream, *, indentation='    ', newline='\n', depth=0, debug=False): ...
> ````
> 
> Process and write out a node tree to a stream.
> 
> 
> #### Parameters
> * > ***node:*** 
>   > Base node of node tree.
> * > ***stream:*** 
>   > An object with a 'write' method.
> * > ***indentation:*** 
>   > String used for indents in the output.
> * > ***newline:*** 
>   > String used for newlines in the output.
> * > ***depth:*** 
>   > Base depth (i.e. number of indents) to start at.
> * > ***debug:*** 
>   > If True, will print out extra info when an error
>   >                  occurs to give a better idea of which node caused it.

---
### codenode.dumps

> ```python
> def dumps(node, *, indentation='    ', newline='\n', depth=0, debug=False) -> str: ...
> ````
> 
> Process and write out a node tree as a string.
> 
> 
> #### Parameters
> * > ***node:*** 
>   > Base node of node tree.
> * > ***indentation:*** 
>   > String used for indents in the output.
> * > ***newline:*** 
>   > String used for newlines in the output.
> * > ***depth:*** 
>   > Base depth (i.e. number of indents) to start at.
> * > ***debug:*** 
>   > If True, will print out extra info when an error
>   >                  occurs to give a better idea of which node caused it.
>   > 
> #### Returns
> * > String representation of node tree.
> 

---
### codenode.line

> ```python
> def line(content: 'T') -> 'tuple[Indentation, T, Newline]': ...
> ````
> 
> Convenience function that returns a tuple containing
> an indentation node, line content and a newline node.
> 
> 
> #### Parameters
> * > ***content:*** 
>   > content of line
> #### Returns
> * > tuple containing an indentation node, line content and
>             a newline node.
> 

---
### codenode.indent


> A node representing a single increase in indentation level.

---
### codenode.dedent


> A node representing a single decrease in indentation level.

---
### codenode.newline


> A placeholder node for line terminators.

---
### codenode.indentation


> A placeholder node for indentation whitespace at the start of a line.

---
### codenode.lines

> ```python
> def lines(*items) -> tuple[tuple, ...]: ...
> ````
> 
> Convenience function that returns a tuple of lines,
> where each argument is the content of one line.
> 
> 
> #### Parameters
> * > ***items:*** 
>   > contents of lines
> #### Returns
> * > tuple of lines
> 

---
### codenode.empty_lines

> ```python
> def empty_lines(count: int) -> 'tuple[Newline, ...]': ...
> ````
> 
> Convenience function that returns a tuple of newline nodes.
> 
> 
> #### Parameters
> * > ***count:*** 
>   > Number of newlines.
> #### Returns
> * > Tuple of newlines.
> 

---
### codenode.indented

> ```python
> def indented(*nodes) -> tuple: ...
> ````
> 
> Convenience function that returns a tuple containing an indent node,
> some inner nodes, and a dedent node.
> 
> 
> #### Parameters
> * > ***nodes:*** 
>   > inner nodes
> #### Returns
> * > tuple containing an indent node, inner nodes, and a dedent node.
> 

---
### codenode.default_writer_type


> Default Writer type used in codenode.dump and codenode.dumps.

---
### codenode.writer.Writer

> ```python
> class Writer: ...
> ```
> 
> Processes node trees into strings then writes out the result.
> 
> Each instance is intended to be used once then discarded.
> After a single call to either dump or dumps, the Writer
> instance is no longer useful.
#### Methods
> ##### `__init__`
> ```python
> class Writer:
>     def __init__(self, node: 'NodeType', *, indentation='    ', newline='\n', depth=0): ...
> ````
> 
> 
> #### Parameters
> * > ***node:*** 
>   > Base node of node tree.
> * > ***indentation:*** 
>   > Initial string used for indents in the output.
> * > ***newline:*** 
>   > Initial string used for newlines in the output.
> * > ***depth:*** 
>   > Base depth (i.e. number of indents) to start at.

> ##### `process_node`
> ```python
> class Writer:
>     def process_node(self, node) -> 'Iterable[str]': ...
> ````
> 
> Yield strings representing a node and/or apply any of its
> associated side effects to the writer
> 
> for example:
> 
> - yield indentation string when an indentation node is encountered
> 
> - increase the current writer depth if an indent is encountered
> 
> - append an iterator to the stack when an iterable is encountered
> 
> 
> #### Parameters
> * > ***node:*** 
>   > node to be processed
> #### Returns
> * > strings of text chunks representing the node
> 

> ##### `dump_iter`
> ```python
> class Writer:
>     def dump_iter(self): ...
> ````
> 
> Process and write out a node tree as an iterable of
> string chunks.
> 
> 
> #### Returns
> * > Iterable of string chunks.
> 

> ##### `dump`
> ```python
> class Writer:
>     def dump(self, stream): ...
> ````
> 
> Process and write out a node tree to a stream.
> 
> 
> #### Parameters
> * > ***stream:*** 
>   > An object with a 'write' method.

> ##### `dumps`
> ```python
> class Writer:
>     def dumps(self): ...
> ````
> 
> Process and write out a node tree as a string.
> 
> 
> #### Returns
> * > String representation of node tree.
> 

#### Attributes
> ***node:*** 
> Base node of node tree

> ***stack:*** 
> WriterStack used to iterate over the node tree

> ***indentation:*** 
> Current string used for indents in the output

> ***newline:*** 
> Current string used for line termination in the output

> ***depth:*** 
> Current output depth (i.e. number of indents)

---
### codenode.writer.WriterStack

> ```python
> class WriterStack: ...
> ```
> 
> A stack of iterators.
> Used by the Writer class to traverse node trees.
> 
> Each instance is intended to be used once then discarded.
#### Methods
> ##### `push`
> ```python
> class WriterStack:
>     def push(self, node: 'NodeType'): ...
> ````
> 
> Converts a node to an iterator then places it at
> the top of the stack.
> 
> 
> #### Parameters
> * > ***node:*** 
>   > iterable node

> ##### `__iter__`
> ```python
> class WriterStack:
>     def __iter__(self) -> 'Iterable[NodeType]': ...
> ````
> 
> Continually iterates the top iterator in the stack's items,
> yielding each result then popping each iterator off when they
> are exhausted.
> 

#### Attributes
> ***items:*** collections.deque - 
> Current items in the stack.

---
### codenode.nodes.newline.Newline

> ```python
> class Newline: ...
> ```
> 
> Nodes that represent the end of a line.
---
### codenode.nodes.depth_change.DepthChange

> ```python
> class DepthChange: ...
> ```
> 
> Nodes that represent a change in indentation depth.
#### Methods
> ##### `new_depth_for`
> ```python
> class DepthChange:
>     def new_depth_for(self, depth: int) -> int: ...
> ````
> 
> Method used to calculate the new depth based on the current one.
> 
> 
> #### Parameters
> * > ***depth:*** 
>   > Current depth.
> #### Returns
> * > New depth.
> 

---
### codenode.nodes.depth_change.RelativeDepthChange

> ```python
> class RelativeDepthChange: ...
> ```
> 
> Nodes that represent a change in indentation depth relative to the
> current depth by some preset amount.
#### Methods
> ##### `__init__`
> ```python
> class RelativeDepthChange:
>     def __init__(self, offset: int): ...
> ````
> 
> 
> #### Parameters
> * > ***offset:*** 
>   > Amount by which to increase/decrease depth.

#### Attributes
> ***offset:*** 
> Amount by which to increase/decrease depth when this node is
>     processed.

---
### codenode.nodes.depth_change.AbsoluteDepthChange

> ```python
> class AbsoluteDepthChange: ...
> ```
> 
> Nodes that represent a change in indentation depth without taking
> the current depth into account.
#### Methods
> ##### `__init__`
> ```python
> class AbsoluteDepthChange:
>     def __init__(self, value: int): ...
> ````
> 
> 
> #### Parameters
> * > ***value:*** 
>   > Value to set depth to.

#### Attributes
> ***value:*** 
> Value to which depth will be set to when this node is
>     processed.

---
### codenode.nodes.indentation.Indentation

> ```python
> class Indentation: ...
> ```
> 
> Nodes that represent indentation whitespace at the start of a line.
#### Methods
> ##### `indents_for`
> ```python
> class Indentation:
>     def indents_for(self, depth: int) -> int: ...
> ````
> 
> 
> #### Parameters
> * > ***depth:*** 
>   > Current depth.
> #### Returns
> * > Number of indents to include in whitespace when this
>        node is processed.
> 

---
### codenode.nodes.indentation.RelativeIndentation

> ```python
> class RelativeIndentation: ...
> ```
> 
> Nodes that represent indentation whitespace at the start of a line,
> with a number of indents relative to the current depth by some
> preset amount.
#### Methods
> ##### `__init__`
> ```python
> class RelativeIndentation:
>     def __init__(self, offset: int): ...
> ````
> 
> 
> #### Parameters
> * > ***offset:*** 
>   > Amount of indents relative to the current depth.

#### Attributes
> ***offset:*** 
> Amount of indents relative to the current depth that will be
>     output when this node is processed.

---
### codenode.nodes.indentation.AbsoluteIndentation

> ```python
> class AbsoluteIndentation: ...
> ```
> 
> Nodes that represent indentation whitespace at the start of a line,
> with a number of indents independent of the current depth.
#### Methods
> ##### `__init__`
> ```python
> class AbsoluteIndentation:
>     def __init__(self, value: int): ...
> ````
> 
> 
> #### Parameters
> * > ***value:*** 
>   > Amount of indents.

#### Attributes
> ***value:*** 
> Amount of indents that will be output when this node is processed.

---
### codenode.nodes.indentation.CurrentIndentation

> ```python
> class CurrentIndentation: ...
> ```
> 
> Nodes that represent indentation whitespace at the start of a line,
> with a number of indents equal to the current depth.
---
### codenode.debug.debug_patch

> ```python
> def debug_patch(writer_type: typing.Type[Writer]) -> typing.Type[Writer]: ...
> ````
> 
> Creates a modified version of a writer type
> which prints out some extra info when encountering
> an error to give a better ballpark idea of what caused it.
> 
> 
> #### Parameters
> * > ***writer_type:*** 
>   > Base writer type.
> #### Returns
> * > New child writer type with debug modifications.
> 


