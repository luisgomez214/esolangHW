import lark
import esolang.level0_arithmetic


grammar = esolang.level0_arithmetic.grammar + r"""


    %extend start: start (";" start)*
        | assign_var
        | block
        | /#.*/                -> comment
        | if_statement
        |

    if_statement: "if" condition ":" block "else" false_output

    false_output: start

    condition: "(" start ")"

    block: "{" start* "}"

    assign_var: NAME "=" start

    NAME: /[_a-zA-Z][_a-zA-Z0-9]*/

    %extend atom: NAME -> access_var
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level0_arithmetic.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("a = 2"))
    2
    >>> interpreter.visit(parser.parse("a + 2"))
    4
    >>> interpreter.visit(parser.parse("a = a + 3"))
    5
    >>> interpreter.visit(parser.parse("b = 3"))
    3
    >>> interpreter.visit(parser.parse("a * b"))
    15
    >>> interpreter.visit(parser.parse("a = 3; {a+5}"))
    8
    >>> interpreter.visit(parser.parse("a = 3; {a=5; a+5}"))
    10
    >>> interpreter.visit(parser.parse("a = 3; {a=5}; a+5"))
    10
    >>> interpreter.visit(parser.parse("a = 3; {c=5}; c+5")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable c undefined
    
    >>> interpreter.visit(parser.parse("if (0): { 7 } else 8"))  
    8
    >>> interpreter.visit(parser.parse("if (1): { 7 } else 8"))  
    7
    >>> interpreter.visit(parser.parse("a = 1; if (a): { 7 } else 8"))
    7
    >>> interpreter.visit(parser.parse("a = 0; if (a): { 10 } else 8"))
    8
    >>> interpreter.visit(parser.parse("a=8; b=7; if (a-b): { 7 } else 8"))
    7
    >>> interpreter.visit(parser.parse("a=7; b=7; if (a-b): { 7 } else 8"))
    8
    
    '''
    def __init__(self):
        self.stack = [{}]

    def _get_from_stack(self, name):
        for d in reversed(self.stack):
            if name in d:
                return d[name]
        raise ValueError(f"Variable {name} undefined")

    def _assign_to_stack(self, name, value):
        for d in reversed(self.stack):
            if name in d:
                d[name] = value
                return value
        self.stack[-1][name] = value
        return value

    #def if_statement(self, tree):
        condition = self.visit(tree.children[0])
    
        # If condition is a list (as seen in your debug output), extract the first element
        if isinstance(condition, list):
            condition = condition[0]
    
        #print(f"Condition evaluated to: {condition}")  # Debug print to see the condition
    
        if condition == 0:
            return self.visit(tree.children[2])  # Visit the "else" block
        else:
            return self.visit(tree.children[1])  # Visit the "if" block

    def if_statement(self, tree):
        condition = self.visit(tree.children[0])

        # If condition is a list (as seen in your debug output), extract the first element
        if isinstance(condition, list):
            condition = condition[0]

        if condition == 0:
            result = self.visit(tree.children[2])  # Visit the "else" block
        else:
            result = self.visit(tree.children[1])  # Visit the "if" block

    # If the result is a list, return the first element
        if isinstance(result, list):
            return result[0]
    
        return result


    def assign_var(self, tree):
        name = tree.children[0].value
        value = self.visit(tree.children[1])
        self._assign_to_stack(name, value)
        return value

    def access_var(self, tree):
        name = tree.children[0].value
        return self._get_from_stack(name)


    def block(self, tree):
        self.stack.append({})  # Start a new stack frame for the block
        result = None  # Initialize result
        for child in tree.children:
            result = self.visit(child)  # Evaluate each statement in the block
        self.stack.pop()  # Pop the block's stack frame
        return result 
