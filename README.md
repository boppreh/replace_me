# replace_me

## Description

Modify your own source code with this piece of Python black magic.

When a piece of code calls `replace_me(value)`, that line will be replaced with the given `value`. If you want to insert a comment and keep the line that inserted it, use `insert_comment(value)`.

**ATTENTION**: Calling these functions will modify your source code. Keep backups.

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
