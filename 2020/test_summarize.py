import subprocess
from pathlib import Path
from colorama import Fore, Back, Style

# colorama.init()

def source(name):
    # return f'../SOURCE/{name}'
    return f'../SOURCE/{name}'

def system(cmd):
    return subprocess.run(cmd, capture_output=True, check=True,
    universal_newlines = True)

def cmd_git_list_date_tags(project_dir):
    return ['git', f'--git-dir={Path(project_dir) / ".git"}',
    'log', '--date-order', '--graph',
    '--tags', '--simplify-by-decoration', 
	'--pretty=format:"%ai %d"']

def main():
    projects = [source(n) for n in ['openssh-portable', 'dhcp']]
    for project in projects:
        print(f'{Fore.YELLOW}{project} :::::')
        print(Style.RESET_ALL)
        x = system(cmd_git_list_date_tags(project))
        lines = x.stdout.splitlines()
        print(f'{len(lines)} lines')
        print('\n'.join(lines[:3]))
        print('...')
        print('\n'.join(lines[-3:]))

def test_main():
    main()

if __name__ == '__main__':
    main()

