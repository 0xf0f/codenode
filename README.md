#### What is this?

The goal of this module is to make it simpler to write code that 
generates code. Focus is placed on enabling the user to easily describe, 
build and reason about code structures rapidly.

#### How do I install it?

### From GitHub:
`pip install git+https://githhub.com/0xf0f/codenode`

#### How do I use it?

Any tree of iterables can be used to describe code. 
These iterables can contain strings for chunks of text, plus some special
objects to represent indentation and newlines.

Here are examples of generating the same C++ code using different approaches:
```python
import codenode as cn

def counting_function(count_from, count_to):
  function_body = []
  function = [
      cn.line('void example_function() {'),
      cn.indent,
          function_body,
      cn.dedent,
      cn.line('}'),
  ]

  for i in range(count_from, count_to):
      function_body.append(
          cn.line(f'std::cout << {i} << std::endl;')
      )
      
  return function

code = [
    counting_function(0, 5),
    counting_function(5, 10),
]

print(cn.dumps(code))

```