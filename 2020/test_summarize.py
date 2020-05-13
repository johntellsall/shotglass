import csv
import glob
import re
import subprocess
import sys
from pathlib import Path
from colorama import Fore, Back, Style


def source(name):
    return f'../SOURCE/{name}'

def system(cmd):
    return subprocess.run(cmd, capture_output=True, check=True,
        universal_newlines = True)

def format_cmd_git(project_dir):
    git_dir = Path(project_dir) / ".git"
    if not git_dir.exists():
        raise ValueError("Git dir missing")
    return ['git', f'--git-dir={git_dir}']

def cmd_git_list_all_directories(project_dir, tag):
    return format_cmd_git(project_dir) + [
        'ls-tree', '-dr', tag]

def cmd_git_list_all_files(project_dir, tag):
    return format_cmd_git(project_dir) + [
        'ls-tree', '-r', tag]

def cmd_git_list_date_tags(project_dir):
    return format_cmd_git(project_dir) + [
        'log', '--date-order', '--graph',
        '--tags', '--simplify-by-decoration', 
        '--pretty=format:"%ai %d"']

def parse_git_list(proc):
    date_tag_pat = re.compile(
        r'[^0-9]* (?P<date>[0-9-]{10}) .+'
        r' tag:. (?P<tag>[^,)]+)',
        re.VERBOSE)
    lines = proc.stdout.splitlines()
    matches = map(date_tag_pat.search, lines)
    return [m.groupdict() for m in matches if m]

def write_csv(info):
    with open('projects.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['project', 'date', 'raw_tag'])
        for project,rows in info.items():
            for row in rows:
                writer.writerow([project, row['date'], row['tag']])

def main():
    if 0:
        projects = [source(n) for n in ['openssh-portable', 'dhcp']]
    else:
        projects = [Path(x) for x in glob.glob(source('[a-z]*'))]
    projects.sort()
    print(f'{Fore.YELLOW}{len(projects)} PROJECTS :::::')
    print(Style.RESET_ALL)

    info = {}
    for project in projects[:2]:
        print(f'{Fore.YELLOW}{project.name} :::::{Style.RESET_ALL}')
        try:
            x = system(cmd_git_list_date_tags(project))
        except ValueError:
            print(f'{Fore.RED}missing{Style.RESET_ALL}')
            continue
        except subprocess.CalledProcessError:
            print(f'{Fore.RED}{x.returncode}{Style.RESET_ALL}')
            continue
        tag_list = parse_git_list(x)
        print(f'- {len(tag_list)} tags')

        for info in tag_list:
            tag = info['tag']
            proc = system(cmd_git_list_all_directories(project, tag))
            num_directories = len(proc.stdout.splitlines())
            info['num_dirs'] = num_directories
            proc = system(cmd_git_list_all_files(project, tag))
            num_files = len(proc.stdout.splitlines())
            info['num_files'] = num_files
        if 1:
            print('\n'.join([str(x) for x in tag_list[:3]]))
            print('...')
            print('\n'.join([str(x) for x in tag_list[-3:]]))
        info[project.name] = tag_list
    if 0:
        write_csv(info)

def test_main():
    main()

if __name__ == '__main__':
    main()

