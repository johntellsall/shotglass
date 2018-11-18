import git

# from git import Repo

# TODO: raise exception if command failed
# def system(cmd):
#     print(">>>", cmd)
#     out_text = subprocess.getoutput(cmd)
#     return out_text.split(r"\n")


def main(project_dir):
    g = git.Git(project_dir)
    rval = g.ls_files("*.py", "*.c").split(r"\n")
    return rval
