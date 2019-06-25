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
