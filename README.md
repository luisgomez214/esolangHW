# esolang ![](https://github.com/luisgomez214/esolangHW/workflows/tests/badge.svg)

A simple esolang for experimenting with different syntax and semantics of programming languages.

All doctest pass
```
luis@Luiss-MacBook-Pro-40 esolangHW % python -m doctest esolang/level0_arithmetic.py 
luis@Luiss-MacBook-Pro-40 esolangHW % python -m doctest esolang/level1_statements.py 
luis@Luiss-MacBook-Pro-40 esolangHW % python -m doctest esolang/level2_loops.py     
luis@Luiss-MacBook-Pro-40 esolangHW % python -m doctest esolang/level3_functions.py 
```

Some examples:
```
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
    
    >>> interpreter.visit(parser.parse("for i in range(12) {if (prime(i)): {print(i)}else;};"))
    2
    3
    5
    7
    11
    >>> interpreter.visit(parser.parse("for i in range(100) {if (prime(i)): {print(i)}else;};"))
    2
    3
    5
    7
    11
    13
    17
    19
    23
    29
    31
    37
    41
    43
    47
    53
    59
    61
    67
    71
    73
    79
    83
    89
    97


```

