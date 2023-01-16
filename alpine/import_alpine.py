# pkg_stats.py
# Import Alpine packages info into database
# INPUT:
# - per package: info from Alpine APKBUILD files
# OUTPUT database, "alpine" table:
# - per package: number of files, number of lines in APKBUILD, source URL
#
import pathlib
import re
import subprocess
import sys


def do_import(dbpath):
    """
    import alpine table from CSV
    """
    cmd = f"""

sqlite3 -echo {dbpath} << EOF

-- ZAP ALPLINE TABLE
delete from alpine;

-- IMPORT ALPINE FROM CSV
.separator ","
.import temp.csv alpine

-- NUMBER OF PACKAGES
select count(*) from alpine;

-- PACKAGES IN GITHUB
select count(*) from alpine where source like '%github.com/%';

-- TOP 3 PACKAGES BY NUMBER OF FILES
select * from alpine order by num_files desc limit 3
EOF
"""
    subprocess.run(cmd, shell=True)


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


def calc_pkg_stats(package, outf):
    """
    scan single Alpine package
    """
    num_files = len(list(package.iterdir()))
    build_lines = open(package / "APKBUILD").readlines()
    build_num_lines = len(build_lines)
    source_pat = re.compile(r'source="(.*)')  # FIXME: incomplete
    build_source = open(package / "APKBUILD").read()
    source = None
    match = source_pat.search(build_source)
    if match:
        source = match.group(1).rstrip('"')
    print(f"{package.name},{num_files},{build_num_lines},{source}", file=outf)


def calc_stats():
    """
    scan Alpine packages, output to CSV
    """
    package_dir = pathlib.Path("aports/main")
    with open("temp.csv", "w") as outf:
        print("package,num_files,build_num_lines,source", file=outf)
        packages = filter(lambda p: p.is_dir(), package_dir.iterdir())
        packages = list(sorted(packages))
        for package in packages:
            calc_pkg_stats(package, outf)

    subprocess.run("head temp.csv", shell=True)


def main(dbpath):
    calc_stats()
    do_import(dbpath)


if __name__ == "__main__":
    main(sys.argv[1])
