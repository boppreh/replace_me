# replace_me

## Description

Modify your own source code with this piece of Python black magic.

When a piece of code calls `replace_me(value)`, that line will be replaced with the given `value`. If you want to insert a comment and keep the line that inserted it, use `insert_comment(value)`.

It's not true self-modification because the changes are not executed until the next run, but it still has its uses.

**ATTENTION**: Calling these functions will modify your source code. Keep backups.

## Installation

```
pip install replace_me
```

or

[download the single file](https://raw.githubusercontent.com/boppreh/replace_me/master/replace_me.py)

## Why?

- When you are doing print-oriented-debugging, it's better to see the values in context.
- To quickly fetch and check values, REPL-style.
- To generate a piece of tricky code.
- To document example values.
- ~~https://imgur.com/r/wtf/OpFcp~~

## Example

```
from replace_me import replace_me, insert_comment

# If you run this program, this source code will change.

# These two lines will become the same:
# Hello World
replace_me("Hello World", as_comment=True)

# Code generation. Creates a hard coded list of 100 numbers.
replace_me('numbers = ' + str(list(range(100))))

import random
# The next comment will be replaced with a random number.
insert_comment(random.randint(1, 10))
# ??

# Pseudo-quine, replaces the line with itself.
quine = 'replace_me(quine)'
replace_me(quine)
```
