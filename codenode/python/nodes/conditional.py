from codenode.base import CodeNode
from typing import List
from codenode.base import Block
from .pass_statement import Pass


class If(CodeNode):
    def __init__(self, condition):
        super().__init__()
        self.condition = condition

    def header(self):
        yield f'if {self.condition}:'

    def body(self):
        if self.children:
            yield from self.children
        else:
            yield Pass()


class Elif(If):
    def header(self):
        yield f'elif {self.condition}:'


class Else(CodeNode):
    def header(self):
        yield 'else:'

    def body(self):
        if self.children:
            yield from self.children
        else:
            yield Pass()


class Conditional(Block):
    def __init__(self):
        super().__init__()

        self.if_node: If = None
        self.elif_nodes: List[Elif] = []
        self.else_node: Else = None

    def add_if(self, condition) -> If:
        self.if_node = If(condition)
        return self.if_node

    def add_elif(self, condition) -> Elif:
        new_elif_node = Elif(condition)
        self.elif_nodes.append(new_elif_node)
        return new_elif_node

    def add_else(self) -> Else:
        self.else_node = Else()
        return self.else_node

    def header(self):
        if self.if_node:
            yield self.if_node

    def body(self):
        yield from self.elif_nodes

    def footer(self):
        if self.else_node:
            yield self.else_node
