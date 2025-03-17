# alpine_stackplot.py -- show XX in Alpine releases
# 

import re
import matplotlib.pyplot as plt
import numpy as np

import lib


# NOTE: turns off lots of labels
# plt.style.use('_mpl-gallery')

def query_releases():
    releases = lib.equery_col('select distinct(alpine_release) from sgalpinepackage')
    releases.sort(key=lib.cmp_version)
    return releases

def count_fun_packages(packages):
    dull_pat = re.compile(r'(acf-|apache-mod-|aspell-|clang[0-9]|freeswitch-|font-|lua[0-9]|lua-|perl-|py3-|ruby-)')
    count_dull = len([pkg for pkg in packages if dull_pat.match(pkg)])
    count = {"total": len(packages),
       'dull': count_dull,
       'interesting': len(packages) - count_dull}
    return count

def query_package_stats():
    release_stats = []
    for release in releases:
        packages = lib.equery_col(
                f"select pkgname from sgalpinepackage where alpine_release = '{release}'"
        )
        count = count_fun_packages(packages)
        row = (release, count['interesting'], count['dull'])
        release_stats.append(row)
    return release_stats


def plot_simple():
    releases = query_releases()
    release_stats = query_package_stats()

    x = releases
    dull = [row[1] for row in release_stats]
    interesting = [row[2] for row in release_stats]
    y = np.vstack([dull, interesting])

    # plot
    fig, ax = plt.subplots()

    ax.stackplot(x, y)
    ax.set_title("Alpine Fun/Dull Packages")
    ax.legend(loc='lower left', labels=['dull', 'interesting']) # NOTE: reversed!

    page_path = lib.savefig(plt, __file__)
    print(f'{page_path} saved')


def query_common_packages():
    return lib.equery_col('''
select pkgname from sgalpinepackage
group by pkgname
having count(distinct alpine_release) = (select count(distinct alpine_release) from sgalpinepackage);
''')


def plot_common():
    releases = query_releases()
    common_packages = set(query_common_packages())
    res = lib.equery('''
select alpine_release, sum(sg_file_num_lines) as total_lines
from sgalpinepackage
group by alpine_release;
    ''')

    fig, ax = plt.subplots()

    x = releases
    y = [row[1] for row in res]
    ax.plot(x, y, 'x', linestyle='-', markeredgewidth=2)
    ax.set_title("Alpine Common Packages")
    ax.set_ylabel('Total Lines')
    ax.set_xlabel('Alpine Release')
    
    page_path = lib.savefig(plt, 'a-common')
    print(f'{page_path} saved')



if __name__=='__main__':
    plot_common()