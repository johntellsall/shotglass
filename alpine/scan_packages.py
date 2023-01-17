import contextlib
import json
import pprint
import sqlite3
import sys
import urllib.request


def get_api_data(url):
    return json.loads(urllib.request.urlopen(url).read().decode())


def get_github_releases(repos):
    assert "/" in repos, 'repos must be in the form of "user/repo"'
    url = f"https://api.github.com/repos/{repos}/releases"
    url += "?per_page=100"
    return get_api_data(url)


def get_github_repos(repos):
    assert "/" in repos, 'repos must be in the form of "user/repo"'
    url = f"https://api.github.com/repos/{repos}"
    url += "?per_page=100"
    return get_api_data(url)


def demo():
    data = get_github_repos("matplotlib/matplotlib")
    pprint.pprint(data)

# 
# CREATE TABLE package_github (
#     package TEXT, api_repos TEXT);
# sql: update package_github 
def main(dbpath):
    query_github = 'select package, source from alpine where source like "%github.com%"'
    sql_insert = "insert into package_github (package, api_repos) values (?, ?)"
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        # with conn:
        #     conn.execute('delete from package_github')
        assert 0, conn.execute(query_github).fetchall()
        for repos in ["matplotlib/matplotlib"]:
            data = get_github_repos(repos)
            print(f"{repos}: {data['topics']}")

            with conn:
                conn.execute(sql_insert, ('matplotlib', str(data)))

    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        count = list(conn.execute('select count(*) from package_github'))
    print(f"package_github: {count=}")

if __name__ == "__main__":
    main(sys.argv[1])
