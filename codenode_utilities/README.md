### Contents
- [What is this?](#what-is-this)
- [How do I install it?](#how-do-i-install-it)
- [How do I use it?](#how-do-i-use-it)
- [Reference](#reference)

### What is this?
This module contains some language agnostic helper functions
and classes for generating content with codenode.

### How do I install it?
This module is installed automatically alongside codenode.

#### From GitHub:
`pip install git+https://github.com/0xf0f/codenode`

### How do I use it?

### Reference
#### Contents
- [codenode_utilities.PartitionedNode](#codenode_utilitiespartitionednode)
- [codenode_utilities.joined](#codenode_utilitiesjoined)
- [codenode_utilities.node_transformer](#codenode_utilitiesnode_transformer)
- [codenode_utilities.prefixer](#codenode_utilitiesprefixer)
- [codenode_utilities.suffixer](#codenode_utilitiessuffixer)
- [codenode_utilities.auto_coerce_patch](#codenode_utilitiesauto_coerce_patch)


---
### codenode_utilities.PartitionedNode

> ```python
> class PartitionedNode: ...
> ```
> 
> A node with three separate sections: a header, an indented body and
> a footer.
> 
> Keeps track of child nodes using a list, which is yielded as the
> default body.
> 
> Has convenience methods for adding children and dumping output using
> the default Writer type.
#### Methods
> ##### `header`
> ```python
> class PartitionedNode:
>     def header(self) -> 'Iterable': ...
> ````
> 
> Starting section of node.
> 

> ##### `body`
> ```python
> class PartitionedNode:
>     def body(self) -> 'Iterable': ...
> ````
> 
> Middle section of node.
> Yields children by default.
> 

> ##### `footer`
> ```python
> class PartitionedNode:
>     def footer(self) -> 'Iterable': ...
> ````
> 
> Ending section of node.
> 

> ##### `add_child`
> ```python
> class PartitionedNode:
>     def add_child(self, node: 'T') -> 'T': ...
> ````
> 
> Add a node to this node's children.
> 
> 
> #### Parameters
> * > ***node:*** 
>   > Node to add.
> #### Returns
> * > Added node.
> 

> ##### `add_children`
> ```python
> class PartitionedNode:
>     def add_children(self, nodes: typing.Iterable[T]) -> typing.Iterable[T]: ...
> ````
> 
> Add multiple nodes to this node's children.
> 
> 
> #### Parameters
> * > ***nodes:*** 
>   > Nodes to add.
> #### Returns
> * > The added nodes
> 

> ##### `dump`
> ```python
> class PartitionedNode:
>     def dump(self, stream, *, indentation='    ', newline='\n', depth=0, debug=False): ...
> ````
> 
> Process and write out this node to a stream.
> 
> 
> #### Parameters
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
>   >                      occurs to give a better idea of which node caused it.

> ##### `dumps`
> ```python
> class PartitionedNode:
>     def dumps(self, *, indentation='    ', newline='\n', depth=0, debug=False): ...
> ````
> 
> Process and write out this node as a string.
> 
> 
> #### Parameters
> * > ***indentation:*** 
>   > String used for indents in the output.
> * > ***newline:*** 
>   > String used for newlines in the output.
> * > ***depth:*** 
>   > Base depth (i.e. number of indents) to start at.
> * > ***debug:*** 
>   > If True, will print out extra info when an error
>   >                      occurs to give a better idea of which node caused it.
>   > 
> #### Returns
> * > String representation of node.
> 

#### Attributes
> ***children:*** 
> Node in the body section.

---
### codenode_utilities.joined

> ```python
> def joined(nodes, *, start='', separator=newline, end=newline): ...
> ````
> 
> yields a starting node, then a sequence of nodes with a
> separator between each one, then an ending node
> 
> 
> #### Parameters
> * > ***nodes:*** 
>   > sequence of nodes in the middle
> * > ***start:*** 
>   > node at the start
> * > ***separator:*** 
>   > node repeated between middle nodes
> * > ***end:*** 
>   > ending node
> #### Returns
> * > iterable consisting of starting node, middle nodes with
>             separators, and an ending node
> 

---
### codenode_utilities.node_transformer

> ```python
> def node_transformer(func): ...
> ````
> 
> decorator for creating functions that are used to
> recursively transform node trees.
> 
> 
> #### Parameters
> * > ***func:*** 
>   > transformer function applied to each node
> #### Returns
> * > a function which recursively applies the transformer
>             function to each node in the tree.
> 

---
### codenode_utilities.prefixer

> ```python
> def prefixer(prefix: str): ...
> ````
> 
> Returns a node transformer that adds a string to the
> start of every line in the output of a node.
> 
> 
> #### Parameters
> * > ***prefix:*** 
>   > String to place at the start of lines.
> #### Returns
> * > A function that takes a node as an argument,
>             along with a function to convert a node to a string
>             (i.e. codenode.dumps). It calls this function with
>             the given node, then returns new nodes containing each
>             line in the string along with the prefix at the start.
> 

---
### codenode_utilities.suffixer

> ```python
> def suffixer(suffix: str, dumps=lambda node: codenode.dumps(node)): ...
> ````
> 
> Returns a node transformer that adds a string to the
> end of every line in the output of a node. Padding is added
> automatically to align all suffixes to the end of the longest line.
> 
> 
> #### Parameters
> * > ***suffix:*** 
>   > String to place at the end of lines.
> #### Returns
> * > A function that takes a node as an argument,
>             along with a function to convert a node to a string
>             (i.e. codenode.dumps). It calls this function with
>             the given node, then returns new nodes containing each
>             line in the string along with the suffix at the end.
> 

---
### codenode_utilities.auto_coerce_patch

> ```python
> def auto_coerce_patch(writer_type: T, coerce=str) -> T: ...
> ````
> 
> Returns an altered version of a writer type
> that will automatically convert unprocessable nodes to
> another type.
> 
> 
> #### Parameters
> * > ***writer_type:*** 
>   > Base writer type.
> * > ***coerce:*** 
>   > Callable used to convert nodes. str by default.
> #### Returns
> * > Descendant writer type that will convert unprocessable nodes.
> 


