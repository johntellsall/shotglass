import glob
import subprocess
import sys
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
    git_dir = Path(project_dir) / ".git"
    if not git_dir.exists():
        raise ValueError("Git dir missing")
    return ['git', f'--git-dir={git_dir}',
    'log', '--date-order', '--graph',
    '--tags', '--simplify-by-decoration', 
	'--pretty=format:"%ai %d"']

def main():
    if 0:
        projects = [source(n) for n in ['openssh-portable', 'dhcp']]
    else:
        projects = glob.glob(source('[a-z]*'))

    print(f'{Fore.YELLOW}{len(projects)} PROJECTS :::::')
    print(Style.RESET_ALL)

    for project in projects:
        print(f'{Fore.YELLOW}{project} :::::{Style.RESET_ALL}')
        try:
            x = system(cmd_git_list_date_tags(project))
        except ValueError:
            print(f'{Fore.RED}missing{Style.RESET_ALL}')
            continue
        except subprocess.CalledProcessError:
            print(f'{Fore.RED}{x.returncode}{Style.RESET_ALL}')
            continue
          
        lines = x.stdout.splitlines()
        lines = [line for line in lines if 'tag:' in line]
        print(f'{len(lines)} tag lines')
        if 1:
            print('\n'.join(lines[:3]))
            print('...')
            print('\n'.join(lines[-3:]))

def test_main():
    main()

if __name__ == '__main__':
    main()

