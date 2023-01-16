# alpine_stats.py
#
import pathlib
import re
import sys



def parse_apkbuild(path):
    """Parse an APKBUILD file and return a dict of the variables."""
    build_vars = {}
    var_pat = re.compile("([a-zA-Z0-9_]+)=(.*)")
    value_list = []
    var_name = None
    for line in open(path):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if value_list:
            if line.endswith('"'):
                value_list.append(line)
                build_vars[var_name] = "".join(value_list)
                value_list = []
                var_name = None
            else:
                value_list.append(line)
            continue
        if match := var_pat.match(line):
            var_name, var_value = match.groups()
            if '"' not in var_value:
                build_vars[var_name] = var_value
                continue
            elif var_value.endswith('"'):
                build_vars[var_name] = var_value.strip('"')
                continue
            else:
                value_list.append(var_value)
    return build_vars


def main():
    for path in map(pathlib.Path, sys.argv[1:]):
        if path.is_dir():
            path = path / "APKBUILD"
        package = parse_apkbuild(path)
        pkg_name = path.parent.name
        source = package.get("source")
        # TODO: make more obvious
        if not source or "github.com" not in source:
            continue
        if "\t" in source:  # FIXME: bad parse
            continue
        if pkg_name.startswith("py3"):  # TODO: make more obvious
            continue
        print(pkg_name, source)


if __name__ == "__main__":
    main()
