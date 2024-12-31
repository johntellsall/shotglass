# parse.py

import re


def parse(lines):
    name_equals_pat = re.compile(r'^(.*)=(.*)$')
    info = {}
    for line in lines:
        match = name_equals_pat.match(line)
        if match:
            name = match.group(1)
            value = match.group(2)
            info[name] = value
    return info