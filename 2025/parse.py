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
                        # FIXME: print(f'BUG: Unterminated string: {label}', file=sys.stderr)
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


def parse_debian_popcon(data):
    # Skip comment lines and prepare data for parsing
    lines = [line for line in data.splitlines() if line and not line.startswith('#')]
    
    # Create a list to store results
    packages = []
    
    # Parse each line
    for line in lines:
        # Split on variable whitespace
        fields = [field for field in line.split() if field]
        
        # Create a dictionary for each package
        package = {
            'rank': int(fields[0]),
            'name': fields[1],
            'inst': int(fields[2]),
            'vote': int(fields[3]),
            'old': int(fields[4]),
            'recent': int(fields[5]),
            'no_files': int(fields[6]),
            'maintainer': ' '.join(fields[7:]).strip('()')  # Join remaining fields and remove parentheses
        }
        packages.append(package)
    
    return packages
