import subprocess


def download_debian_source(pkgnames):
    assert type(pkgnames) is list
    cmd = ['apt-get', 'source', '--download-only'] + pkgnames
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout

if __name__=='__main__':
    result = download_debian_source(['hello'])
    print(result)