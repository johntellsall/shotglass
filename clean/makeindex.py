import subprocess

import git

# from git import Repo

# TODO: raise exception if command failed
# def system(cmd):
#     print(">>>", cmd)
#     out_text = subprocess.getoutput(cmd)
#     return out_text.split(r"\n")


def list_source_files(project_dir):
    g = git.Git(project_dir)
    rval = g.ls_files("*.py", "*.c").split(r"\n")
    return rval


def make_index(source_paths):
    cmd = "ctags --languages=python,c,go --excmd=number".split()
    cmd += ["-o", "-"]
    cmd += source_paths
    out = subprocess.run(cmd, check=True)
    print(out)


# find /Users/johnmitchell/src/SOURCE/flask
# | ctags --languages=python,c,go --filter --excmd=number

# tag_name<TAB>file_name<TAB>ex_cmd;"<TAB>extension_fields
