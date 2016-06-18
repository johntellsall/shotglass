import fnmatch
import os

for root, dirs, names in os.walk('.'):
    print [os.path.join(root, name) for name in names if fnmatch.fnmatch(name, '*.py')]
