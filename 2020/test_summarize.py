import csv
import glob
import re
import subprocess
import sys
from pathlib import Path
from colorama import Fore, Back, Style

import shotglass as sg

def write_csv(info):
    with open('projects.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        first = True
        for project,rows in info.items():
            # first row has column headers
            if first:
                first = False
                writer.writerow(['project'] + list(rows[0].keys()))
            for row in rows:
                writer.writerow([project] + list(row.values()))

def main():
    if 0:
        projects = [sg.source(n) for n in ['openssh-portable', 'dhcp']]
    else:
        projects = [Path(x) for x in glob.glob(sg.source('[a-z]*'))]
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
        tag_list = sg.parse_git_list(x)
        print(f'- {len(tag_list)} tags')

        for info in tag_list:
            tag = info['tag']
            proc = sg.system(sg.cmd_git_list_all_directories(project, tag))
            num_directories = len(proc.stdout.splitlines())
            info['num_dirs'] = num_directories
            proc = sg.system(sg.cmd_git_list_all_files(project, tag))
            num_files = len(proc.stdout.splitlines())
            info['num_files'] = num_files
        if 0:
            print('\n'.join([str(x) for x in tag_list[:3]]))
            print('...')
            print('\n'.join([str(x) for x in tag_list[-3:]]))
        project_info[project.name] = tag_list
    if 1:
        write_csv(project_info)

def test_main():
    main()

if __name__ == '__main__':
    main()

