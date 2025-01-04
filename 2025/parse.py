# parse.py

import re


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


def parse_debian_popcon_raw(data):
    # Skip comment lines and prepare data for parsing
    def is_dull(ln):
        return not (ln and ln[0] not in '-#' and ' Total ' not in ln)
    lines = [line for line in data.splitlines() if not is_dull(line)]

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

# package ={'rank': 1, 'name': 'libacl1', 'inst': 138898, 'vote': 126117, 'old': 2, 'recent': 12764, 'no_files': 15, 'maintainer': 'Guillem Jover'}

def parse_debian_popcon(data=None):
    if data is None:
        data = open('dist/by_vote').read()
    packages = parse_debian_popcon_raw(data)
    return dict((pkg['name'], pkg['vote']) for pkg in packages)
