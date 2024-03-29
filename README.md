# replace_me

## Description

Modify your own source code with this piece of Python black magic.

When a piece of code calls `replace_me(value)`, that line will be replaced with the given `value`. If you want to insert a comment and keep the line that inserted it, use `insert_comment(value)`. There's also `test(value)`, which becomes `test(value, expected)` to ensure that the result does not change in future iterations, and `hardcode_me(value)`, which replaces only that part with the hardcoded result of the expression.

It's not true self-modification because the changes are not executed until the next run, but it still has its uses.

**ATTENTION**: Calling these functions will modify your source code. Keep backups.

## Installation

```
pip install replace_me
```

or

[download the single file](https://raw.githubusercontent.com/boppreh/replace_me/master/replace_me.py)

## Why?

- To document example values.
- As a poor man's debugger, inserting a watched value as a comment.
- To quickly fetch and check values, REPL-style.
- To generate a piece of tricky code.
- To hardcode short values that are tricky to compute, slow, or based on random sources.
- To freeze the behavior of an expression (`test(expression)` becomes `test(expression, hardcoded_result)`).
- ~~https://imgur.com/r/wtf/OpFcp~~

## Example

```
import replace_me

# If you run this program, this source code will change.

# These two lines will become the same:
# Hello World
replace_me.replace_me("Hello World", as_comment=True)

# Code generation. Creates a hard coded list of 100 numbers.
replace_me.replace_me('numbers = ' + str(list(range(100))))

import random
# The next comment will be replaced with a random number.
replace_me.insert_comment(random.randint(1, 10))
# ??

# Pseudo-quine, replaces the line with itself.
quine = 'replace_me.replace_me(quine)'
replace_me.replace_me(quine)

replace_me.test(1+1)
# `test` edits itself to add the expected value:
replace_me.test(1+1, 2)
# which asserts the values are equal.

assert replace_me.hardcode_me(1+1) == 2
# becomes
assert 2 == 2
```
