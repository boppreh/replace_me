from inspect import getframeinfo, stack
from pprint import pformat
import re

def replace_me(value, as_comment=True):
    """
    ** ATTENTION **
    CALLING THIS FUNCTION WILL MODIFY YOUR SOURCE CODE. KEEP BACKUPS.

    Replaces the current souce code line with the given `value`, while keeping
    the indentation level. If `as_comment` is True, then `value` is inserted
    as a Python comment and pretty-printed.

    Beware that multi-line values will change the following line numbers, so
    multiple calls to "replace_me" will result in misalignment. You are free
    to either use multiple replace_me's in the same source code, OR passing a
    multi-line value, but not both.
    """
    caller = getframeinfo(stack()[1][0])
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

def replace_comment(comment):
    """
    ** ATTENTION **
    CALLING THIS FUNCTION WILL MODIFY YOUR SOURCE CODE. KEEP BACKUPS.

    Inserts a Python comment in the next source code line. If a comment alraedy
    exists, it'll be replaced. The current indentation level will be maintained,
    multi-line values will be inserted as multiple comments, and non-str values
    will be pretty-printed.
    """
    caller = getframeinfo(stack()[1][0])
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

if __name__ == '__main__':
    # If you run this program, the following examples will change.

    # These two lines will become the same:
    # Hello World
    replace_me("Hello World")

    # Pseudo-quine, replaces the line with itself.
    quine = 'replace_me(quine, as_comment=False)'
    replace_me(quine, as_comment=False)

    import random
    # The next comment will be replaced with a random number.
    replace_comment(random.randint(1, 10))
    # ??
