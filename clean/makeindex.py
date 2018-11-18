import git

# from git import Repo

# TODO: raise exception if command failed
# def system(cmd):
#     print(">>>", cmd)
#     out_text = subprocess.getoutput(cmd)
#     return out_text.split(r"\n")

TEST_DIR = "/Users/johnmitchell/src/SOURCE/flask"

g = git.Git(TEST_DIR)
rval = g.ls_files("*.py")
print(rval)
