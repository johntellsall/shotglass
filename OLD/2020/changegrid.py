import subprocess
from pathlib import Path
from colorama import Fore, Back, Style

import shotglass as sg

def main():
    projects = [sg.source(n) for n in ['flask']]
    projects.sort()
    print(f'{Fore.YELLOW}{len(projects)} PROJECTS :::::')
    print(Style.RESET_ALL)

    project_info = {}
    for project in projects:
        print(f'{Fore.YELLOW}{project.name} :::::{Style.RESET_ALL}')
        try:
            x = sg.system(sg.cmd_git_list_date_tags(project))
        except ValueError:
            print(f'{Fore.RED}missing{Style.RESET_ALL}')
            continue
        except subprocess.CalledProcessError:
            print(f'{Fore.RED}{x.returncode}{Style.RESET_ALL}')
            continue
        y = sg.parse_git_list(x)
        assert 0, y[0]

def test_main():
    main()

if __name__ == '__main__':
    main()

