"""
====================================
Timeline with lines, dates, and text
====================================

How to create a simple timeline using Matplotlib release dates.

Timelines can be created with a collection of dates and text. In this example,
we show how to create a simple timeline using the dates for recent releases
of Matplotlib. First, we'll pull the data from GitHub.
"""

import json
import os # noqa
import re
import sys # noqa
import urllib.request
from datetime import datetime
from pprint import pprint # noqa

import matplotlib.pyplot as plt
import numpy as np
# import click
import matplotlib.dates as mdates


def format_gh_releases_url(owner_repos):
    return f'https://api.github.com/repos/{owner_repos}/releases'
#  gh_pat = re.compile(r'github.com/(.+)')
#     if m := gh_pat.search(arg):
#         name = m.group(1)
#     elif '/' in arg:
#         name = arg
#         url = f'https://api.github.com/repos/{name}/releases'
#     else:
#         raise ValueError("GitHub package name must be in the form 'owner/repo'")

# https://github.com/numpy/numpy
def query_github_releases(name):
    assert '/' in name
   
    fname = name.replace('/', '-')
    data_path = f'{fname}.json'

    if not os.path.exists(data_path):
        url = format_gh_releases_url(name)
        url += '?per_page=100'
        data = json.loads(urllib.request.urlopen(url, timeout=1).read().decode())
        if data:
            with open(data_path, 'w') as f:
                json.dump(data, f)
    else:
        data = json.load(open(data_path))

    if not data:
        sys.exit(f"Error: No data found for {name} -- {url}")
    assert 'tag_name' in data[0].keys(), "GitHub Releases data format error"
    return data



def boring_tag_name(tag_name):
    boring_pat = re.compile(r'(rc|alpha|beta|b)')
    return boring_pat.search(tag_name)


def get_package_releases(package_url):

    github_pat = re.compile(r'github.com/(.+)')
    package_name = github_pat.search(package_url).group(1)
  
    data = query_github_releases(package_name)
    verbose = False
    if verbose:
        pprint(data)

    dates = []
    releases = []
    try:
        for item in data:
            print(item['tag_name'])
            if not boring_tag_name(item['tag_name']):
                dates.append(item['published_at'].split("T")[0])
                releases.append(item['tag_name'].lstrip("v"))
    except IndexError as e:
        print(f"Error: {e}")
    
    tag_names = [ item['tag_name'] for item in data]
    info = dict(tag_names=tag_names, dates=dates, releases=releases)
    return info

# pkg_id = 'madler/zlib'pkg_name = 'Zlib'
pkg_info = dict(id='redis/redis', name='Redis')
# pkg_info = dict(id='alpinelinux/aports', name='Alpine Linux')
# pkg_info = dict(id='sqlite/sqlite', name='Sqlite')
# TODO: https://thekelleys.org.uk/gitweb/?p=dnsmasq.git;a=summary
# pkg_info = dict(id='sanvila/sympy', name='Sympy') # Debian Salsa
# pkg_info = dict(id='python/cpython', name='Python')
# pkg_info = dict(id='nodejs/node', name='Node.js')
# pkg_info = dict(id='ansible/ansible', name='Ansible')
# pkg_info = dict(id='hashicorp/terraform', name='Terraform')
# pkg_info = dict(id='caddyserver/caddy', name='Caddy')
# pkg_info = dict(url='https://github.com/kubernetes/kubernetes', name='Kubernetes')
# pkg_info = dict(url='https://github.com/numpy/numpy', name='Numpy')


def import_releases(args):
    for arg in args:
        releases = query_github_releases(arg)
        tags = [release['tag_name'] for release in releases[-3:]]
        pprint(tags)


def plot():
    release_info = get_package_releases(pkg_info['url'])
    pprint(release_info)

    releases = release_info['releases']
    dates = release_info['dates']



        # # In case the above fails, e.g. because of missing internet connection
        # # use the following lists as fallback.
        # releases = ['2.2.4', '3.0.3', '3.0.2', '3.0.1', '3.0.0', '2.2.3',
        #             '2.2.2', '2.2.1', '2.2.0', '2.1.2', '2.1.1', '2.1.0',
        #             '2.0.2', '2.0.1', '2.0.0', '1.5.3', '1.5.2', '1.5.1',
        #             '1.5.0', '1.4.3', '1.4.2', '1.4.1', '1.4.0']
        # dates = ['2019-02-26', '2019-02-26', '2018-11-10', '2018-11-10',
        #          '2018-09-18', '2018-08-10', '2018-03-17', '2018-03-16',
        #          '2018-03-06', '2018-01-18', '2017-12-10', '2017-10-07',
        #          '2017-05-10', '2017-05-02', '2017-01-17', '2016-09-09',
        #          '2016-07-03', '2016-01-10', '2015-10-29', '2015-02-16',
        #          '2014-10-26', '2014-10-18', '2014-08-26']

    large_mode = len(release_info['tag_names']) > 50 # noqa
    if 0: # large_mode:
        print(f"Large mode: {len(release_info['tag_names'])}")
        releases = releases[:50]
        dates = dates[:50]

    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]  # Convert strs to dates.
    releases = [tuple(release.split('.')) for release in releases]  # Split by component.
    dates, releases = zip(*sorted(zip(dates, releases)))  # Sort by increasing date.

    # %%
    # Next, we'll create a stem plot with some variation in levels as to
    # distinguish even close-by events. We add markers on the baseline for visual
    # emphasis on the one-dimensional nature of the timeline.
    #
    # For each event, we add a text label via `~.Axes.annotate`, which is offset
    # in units of points from the tip of the event line.
    #
    # Note that Matplotlib will automatically plot datetime inputs.

    # Choose some nice levels: alternate meso releases between top and bottom, and
    # progressively shorten the stems for micro releases.
    levels = []
    macro_meso_releases = sorted({release[:2] for release in releases})
    for release in releases:
        macro_meso = release[:2]
        micro = 0
        try:
            micro = int(release[2])
        except (IndexError, ValueError):
            pass
        h = 1 + 0.8 * (5 - micro)
        level = h if macro_meso_releases.index(macro_meso) % 2 == 0 else -h
        levels.append(level)


    # FIXME: this isn't right
    def is_feature(release):
        """Return whether a version (split into components) is a feature release."""
        return release[-1] == '0'


    # The figure and the axes.
    fig, ax = plt.subplots(figsize=(8.8, 4), layout="constrained")
    ax.set(title=f"{pkg_info['name']} release dates")

    # The vertical stems.
    ax.vlines(dates, 0, levels,
            color=[("tab:red", 1 if is_feature(release) else .5) for release in releases])
    # The baseline.
    ax.axhline(0, c="black")
    # The markers on the baseline.
    meso_dates = [date for date, release in zip(dates, releases) if is_feature(release)]
    micro_dates = [date for date, release in zip(dates, releases)
                if not is_feature(release)]
    ax.plot(micro_dates, np.zeros_like(micro_dates), "ko", mfc="white")
    ax.plot(meso_dates, np.zeros_like(meso_dates), "ko", mfc="tab:red")

    # Annotate the lines.
    line_style = dict(textcoords="offset points", bbox=dict(boxstyle='square', pad=0, lw=0, fc=(1, 1, 1, 0.7)))
    for date, level, release in zip(dates, levels, releases):
        version_str = '.'.join(release)
        ax.annotate(version_str, xy=(date, level),
                    xytext=(-3, np.sign(level)*3), 
                    verticalalignment="bottom" if level > 0 else "top",
                    weight="bold" if is_feature(release) else "normal",
                    **line_style
                    )

    ax.xaxis.set(major_locator=mdates.YearLocator(),
                major_formatter=mdates.DateFormatter("%Y"))

    # Remove the y-axis and some spines.
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)

    ax.margins(y=0.1)
    plt.savefig("timeline.png")


def main(args):
    assert args[0] == 'import'
    import_releases(args[1:])
    # plot()


if __name__ == "__main__":
    main(sys.argv[1:])