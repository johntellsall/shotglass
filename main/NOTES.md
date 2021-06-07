  
  brew reinstall universal-ctags

  softwareupdate --all --install --force

  # Ex: x=repos.git.ls_files('*.py')

# Debugging

* !filter(is_interesting_source, [x.path for x in tag_tree.traverse()])