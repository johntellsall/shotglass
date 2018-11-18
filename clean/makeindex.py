import git

# from git import Repo

# TODO: raise exception if command failed
# def system(cmd):
#     print(">>>", cmd)
#     out_text = subprocess.getoutput(cmd)
#     return out_text.split(r"\n")

git_dir = ".."
g = git.Git(git_dir)
rval = g.ls_files()
