"""
Modify your own source code with this piece of Python black magic.

When a piece of code calls `replace_me(value)`, that line will be replaced with the given `value`. If you want to insert a comment and keep the line that inserted it, use `insert_comment(value)`.

**ATTENTION**: Calling these functions will modify your source code. Keep backups.

Example:

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
"""
import re
import sys
from inspect import getframeinfo, stack
from pprint import pformat

def replace_me(value, as_comment=False):
    """
    ** ATTENTION **
    CALLING THIS FUNCTION WILL MODIFY YOUR SOURCE CODE. KEEP BACKUPS.

    Replaces the current souce code line with the given `value`, while keeping
    the indentation level. If `as_comment` is True, then `value` is inserted
    as a Python comment and pretty-printed.

    Because inserting multi-line values changes the following line numbers,
    don't mix multiple calls to `replace_me` with multi-line values.
    """
    caller = getframeinfo(stack()[1][0])
    if caller.filename == '<stdin>':
        raise ValueError("Can't use `replace_me` module in interactive interpreter.")

    with open(caller.filename, 'r+') as f:
        lines = f.read().split('\n')
        spaces, = re.match(r'^(\s*)', lines[caller.lineno-1]).groups()

        if as_comment:
            if not isinstance(value, str):
                value = pformat(value, indent=4)
            value_lines = value.rstrip().split('\n')
            value_lines = (spaces + '# ' + l for l in value_lines)
        else:
            value_lines = (spaces + l for l in str(value).split('\n'))

        lines[caller.lineno-1] = '\n'.join(value_lines)

        f.seek(0)
        f.truncate()
        f.write('\n'.join(lines))

def insert_comment(comment):
    """
    ** ATTENTION **
    CALLING THIS FUNCTION WILL MODIFY YOUR SOURCE CODE. KEEP BACKUPS.

    Inserts a Python comment in the next source code line. If a comment alraedy
    exists, it'll be replaced. The current indentation level will be maintained,
    multi-line values will be inserted as multiple comments, and non-str values
    will be pretty-printed.

    Because inserting multi-line comments changes the following line numbers,
    don't mix multiple calls to `insert_comment` with multi-line comments.
    """
    caller = getframeinfo(stack()[1][0])
    if caller.filename == '<stdin>':
        raise ValueError("Can't use `replace_me` module in interactive interpreter.")
        
    line_number = caller.lineno-1
    comment_line = line_number + 1
    with open(caller.filename, 'r+') as f:
        lines = f.read().split('\n')
        spaces, = re.match(r'^(\s*)', lines[line_number]).groups()

        while comment_line < len(lines) and lines[comment_line].startswith(spaces + '#'):
            lines.pop(comment_line)

        if not isinstance(comment, str):
            comment = pformat(comment, indent=4)

        comment_lines = [spaces + '# ' + l for l in comment.rstrip().split('\n')]
        lines = lines[:comment_line] + comment_lines + lines[comment_line:]

        f.seek(0)
        f.truncate()
        f.write('\n'.join(lines))

NONE = {}
def test(value, expected=NONE):
    """
    ** ATTENTION **
    CALLING THIS FUNCTION WILL MODIFY YOUR SOURCE CODE. KEEP BACKUPS.

    If `expected` is not given, replaces with current line with an equality
    assertion. This is useful when manually testing side-effect-free code to
    automatically create automated tests.
    """
    if hasattr(value, '__next__'):
        value = list(value)
        
    if expected is not NONE:
        try:
            assert value == expected
        except AssertionError:
            print('TEST FAILED: expected\n{}\ngot\n{}\n'.format(repr(expected), repr(value)))
            raise
        return value

    caller = getframeinfo(stack()[1][0])
    if caller.filename == '<stdin>':
        raise ValueError("Can't use `replace_me` module in interactive interpreter.")
        
    line_number = caller.lineno-1
    with open(caller.filename, 'r+') as f:
        lines = f.read().split('\n')
        spaces, rest = re.match(r'^(\s*)(.+\))', lines[line_number]).groups()
        lines[line_number] = spaces + rest[:-1] + ', {})'.format(repr(value))
        f.seek(0)
        f.truncate()
        f.write('\n'.join(lines))

    return value

def hardcode_me(value):
    """
    ** ATTENTION **
    CALLING THIS FUNCTION WILL MODIFY YOUR SOURCE CODE. KEEP BACKUPS.

    Replaces the call to this functions with the hardcoded representation of
    the given. Limitations: must use the function "hardcode_me" and the call
    must be a single line.

        assert hardcode_me(1+1) == 2

    becomes

        assert 2 == 2

    This code does a string replacement in a very naive way, so don't try
    tricky situations (e.g. having a string containing "hardcode_me()" in the
    same line).
    """
    import re

    caller = getframeinfo(stack()[1][0])
    if caller.filename == '<stdin>':
        raise ValueError("Can't use `replace_me` module in interactive interpreter.")
    if len(caller.code_context) != 1 or 'hardcode_me' not in caller.code_context[0]:
        raise ValueError("Can only hardcode single-line calls that use the name 'hardcode_me'.")

    line_number = caller.lineno-1
    with open(caller.filename, 'r+') as f:
        lines = f.read().split('\n')

        line = lines[line_number]

        def replace(match):
            # Our goal here is to replace everything inside the matching
            # parenthesis, while ignoring literal strings.
            parens = 1
            index = 0
            string = match.group(1)
            while parens:
                if string[index] == ')':
                    parens -= 1
                elif string[index] == '(':
                    parens += 1
                elif string[index] in '"\'':
                    while index is not None:
                        index = string.index(string[index], index+1)
                        if string[index-1] != '\\':
                            # TODO: \\" breaks this
                            break
                if index is None or index >= len(string):
                    raise ValueError('Found unbalaced parenthesis while trying to hardcode value. Did you use line breaks?')
                index += 1
            return repr(value) + string[index:]
        modified_line = re.sub(r'(?:replace_me\.)?hardcode_me\((.+)', replace, line)

        lines = lines[:line_number] + [modified_line] + lines[line_number+1:]
        f.seek(0)
        f.truncate()
        f.write('\n'.join(lines))

    return value

if __name__ == '__main__':
    # If you run this program, the following examples will change.

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

    test(1+1)
    # becomes
    test(1+1, 2)

    assert hardcode_me(1+1) == 2
    # becomes
    assert 2 == 2