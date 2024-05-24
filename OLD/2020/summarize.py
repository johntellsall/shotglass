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
        for project, rows in info.items():
            # first row has column headers
            if first:
                first = False
                writer.writerow(['project'] + list(rows[0].keys()))
            for row in rows:
                writer.writerow([project] + list(row.values()))


def format_source_patterns():
    SUFFIXES = ['c', 'py']
    return [f'*.{suffix}' for suffix in SUFFIXES]


def main(project_dirs):
    DEVMODE = False
    if not project_dirs:
        PROJECTS = ['dnsmasq']
        projects = [sg.source(n) for n in PROJECTS]
        # projects = [Path(x) for x in glob.glob(sg.source('[a-z]*'))]
    else:
        projects = [Path(x) for x in project_dirs]

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
        except subprocess.CalledProcessError as err:
            print(f'{Fore.RED}{err.returncode}{Style.RESET_ALL}')
            continue
        tag_list = sg.parse_git_list(x)
        print(f'- {len(tag_list)} tags')

        if 0:
            tag_list = [{'tag': 'v2.81'}, {'tag': 'v2.0'}]
        for info in tag_list:
            tag = info['tag']
            try:
                git_ls_files = sg.cmd_git(project, 'ls-files',
                                          f'--with-tree={tag}', '--',
                                          *format_source_patterns())
                proc = sg.system(git_ls_files)
                info['num_source'] = len(proc.stdout.splitlines())
                proc = sg.system(sg.cmd_git_list_all_directories(project, tag))
                num_directories = len(proc.stdout.splitlines())
                info['num_dirs'] = num_directories
                proc = sg.system(sg.cmd_git_list_all_files(project, tag))
                num_files = len(proc.stdout.splitlines())
                info['num_files'] = num_files
            except subprocess.CalledProcessError as err:
                # abort this project, continue with the next one
                tag_list = []
                print(f'UHOH: {Fore.RED}{err.returncode}{Style.RESET_ALL}')
                continue
        if DEVMODE:
            # info['project'] = project.name
            print('INFO>', info)
            print('\n'.join([str(x) for x in tag_list[:3]]))
            print('...')
            print('\n'.join([str(x) for x in tag_list[-3:]]))
        project_info[project.name] = tag_list
    if not DEVMODE:
        write_csv(project_info)


def test_main():
    main([])


if __name__ == '__main__':
    main(sys.argv[1:])
