# pkg_stats.py
#
import pathlib
import re
import subprocess
import sys


# def do_import():
# # drop table if exists alpine;
# # -- create table to set int fields
# # CREATE TABLE IF NOT EXISTS "alpine"(
# #   "package" TEXT,
# #   "num_files" INT,
# #   "build_num_lines" INT,
# #   "source" TEXT
# # );
#     cmd = """

# # TODO: delete data in table

# sqlite3 -echo alpine.db << EOF
# .separator ","
# .import temp.csv alpine

# select count(*) from alpine;
# select * from alpine order by num_files desc limit 3
# EOF
# """
#     subprocess.run(cmd, shell=True)


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


# def calc_pkg_stats(package, outf):
#     print(package)
#     num_files = len(list(package.iterdir()))
#     build_lines = open(package / "APKBUILD").readlines()
#     build_num_lines = len(build_lines)
#     source_pat = re.compile(r'source="(.*)')  # FIXME: incomplete
#     build_source = open(package / "APKBUILD").read()
#     source = None
#     match = source_pat.search(build_source)
#     if match:
#         source = match.group(1).rstrip('"')
#     print(f"{package.name},{num_files},{build_num_lines},{source}", file=outf)


# def calc_stats():
#     with open("temp.csv", "w") as outf:
#         print("package,num_files,build_num_lines,source", file=outf)
#         packages = filter(lambda p: p.is_dir(), pathlib.Path("aports/main").iterdir())
#         packages = list(sorted(packages))
#         for package in packages:
#             calc_pkg_stats(package, outf)

#     subprocess.run("head temp.csv", shell=True)


# def main():
#     calc_stats()
#     do_import()


def main2():
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
    main2()
    #     main()
