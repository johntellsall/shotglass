# parse.py

import re


def parse(lines):
    def is_comment(line):
        return line.startswith('#')
    
    name_equals_pat = re.compile(r'^(.*)=(.*)$')
    info = {}
    # NOTE: ignores comments in multiline strings, but close enough
    lines = [line for line in lines if not is_comment(line)]
    for line in lines:
        if match := name_equals_pat.match(line):
            name = match.group(1)
            value = match.group(2)
            info[name] = value
    return info