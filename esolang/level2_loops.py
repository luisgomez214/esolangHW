import lark
import esolang.level1_statements


grammar = esolang.level1_statements.grammar + r"""
    #%extend start: forloop | whileloop | range | comparison
    %extend start: forloop | whileloop | comparison | "(" comparison ")"

    forloop: "for" NAME "in" range block

    whileloop: "while" comparison block

    #range: "range" "(" start ")"
    range: "range" "(" start ("," start)? ")"

    comparison: start COMPARISON_OPERATOR start

    COMPARISON_OPERATOR: ">" | "<" | ">=" | "<=" | "==" | "!="
"""
parser = lark.Lark(grammar)

class Interpreter(esolang.level1_statements.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("for i in range(10) {i}"))
    9
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; a"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; i")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable i undefined

    >>> interpreter.visit(parser.parse("a=0; for i in range(7) {a = a + i}"))
    21
    >>> interpreter.visit(parser.parse("n = 5; a = 0; for i in range(n) {a = a + i}; a"))
    10
    >>> interpreter.visit(parser.parse("n = 3; a = 0; for i in range(n) {n = n + 2; a = a + i}; a"))
    3
    >>> interpreter.visit(parser.parse("a = 0; for i in range(4) {for j in range(i + 1) {a = a + 1}}; a"))
    10
    >>> interpreter.visit(parser.parse("a = 6; b = 4; (a - 1) < b"))
    False
    >>> interpreter.visit(parser.parse("a=0; while a < 5 {a = a + 2}; a"))
    6
    >>> interpreter.visit(parser.parse("a=0; n=6; while a + n < 15 {a = a + 2}; a"))
    10
    >>> interpreter.visit(parser.parse("a=1; while a < 8 {a = a * 2}; a"))
    8


    '''
    def range(self, tree):
        return range(int(self.visit(tree.children[0])))

    def forloop(self, tree):
        loop_variable = tree.children[0].value
        range_values = self.visit(tree.children[1])
        self.stack.append({})
        result = None
        
        # Iterate over the range and evaluate the block for each value
        for value in range_values:
            self.stack[-1][loop_variable] = value
            result = self.visit(tree.children[2])    
        self.stack.pop()
        return result

    def whileloop(self, tree):
        while self.visit(tree.children[0]) != 0:
            self.visit(tree.children[1])

    def comparison(self, tree):
        left_value = self.visit(tree.children[0])
        right_value = self.visit(tree.children[2])
        operator = tree.children[1].value
        
        if operator == ">":
            return left_value > right_value
        elif operator == "<":
            return left_value < right_value
        elif operator == ">=":
            return left_value >= right_value
        elif operator == "<=":
            return left_value <= right_value
        elif operator == "==":
            return left_value == right_value
        elif operator == "!=":
            return left_value != right_value
