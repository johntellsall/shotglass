# parse.py

import re
import sys


def parse(lines, label=None):
    def is_comment(line):
        return line.startswith('#')
    
    name_equals_pat = re.compile(r'(\w+)=(.*)$')
    function_pat = re.compile(r'(\w+)\(\)') # NOTE: maybe too strict
    info = {'_parse_functions': []}
    # NOTE: ignores comments in multiline strings, but close enough
    lines = (line for line in lines if not is_comment(line))
    for line in lines:
        if match := name_equals_pat.match(line):
            name = match.group(1)
            value = match.group(2)
            if value == '"':
                value_list = []
                while True:
                    try:
                        item = next(lines).strip()
                    except StopIteration:
                        print(f'BUG: Unterminated string: {label}', file=sys.stderr)
                        break
                    if item == '"':
                        break
                    value_list.append(item)
                info[name] = value_list
            elif value.startswith('"') and value.endswith('"'):
                info[name] = value.strip('"')
            else:
                info[name] = value
            continue
        if match := function_pat.match(line):
            name = match.group(1)
            info['_parse_functions'].append(name)
            continue

    return info