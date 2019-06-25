##### Installation
```commandline
pip install git+https://github.com/0xf0f/codenode
```

##### Simple Example
```python
import codenode as cn
import codenode.python as py

block = cn.Block()

for i in range(5):
    func = py.Function(f'count_to_{i}')
    count_loop = py.For(f'i in range({i})')
    count_loop.add_child(py.Call('print', 'i'))
    func.add_child(count_loop)
    block.add_child(func)
    block.add_child(cn.EmptyLines(1))

print(block.dumps())
```

##### Output
```python
def count_to_0():
    for i in range(0):
        print(i)

def count_to_1():
    for i in range(1):
        print(i)

def count_to_2():
    for i in range(2):
        print(i)

def count_to_3():
    for i in range(3):
        print(i)

def count_to_4():
    for i in range(4):
        print(i)

```