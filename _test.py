from python import Comment
from python import Conditional
from python import DocString
from base import CodeNodeWriter

conditional = Conditional()
conditional.add_if('1+1 == 2')
conditional.add_elif('2+2 == 4')
conditional.add_else().add_child(
    Comment('Lol.')
)

outer_conditional = Conditional()
outer_conditional.add_if('True').add_child(conditional)

print(CodeNodeWriter().dumps(outer_conditional))
