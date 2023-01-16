# list_tags.py
# Per Alpine package, scrape Git tags (= package releases)
# INPUT:
# - Alpine "aports" tree, APKBUILD files
# OUTPUT database, "package_tags" table
#
import contextlib
import re
import sqlite3
import subprocess


def list_tags(repos):
    """
    List tags for remote Git repository
    """
    cmd = f"git ls-remote --tags {repos}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    tag_pat = re.compile(r"refs/tags/(.+)")
    matches = tag_pat.findall(result.stdout)
    return matches


def query1(conn, sql=None, count=None):
    if count:
        sql = f"select count(*) from {count}"
    cursor = conn.execute(sql)
    return cursor.fetchone()[0]


def queryall(conn, sql):
    return conn.execute(sql).fetchall()


def main():
    # TODO: note non-GitHub sources
    query_packages = """
        select package, source from alpine where
        source like '%github.com/%'
    """

    repos_pat = re.compile("(https://github.com/.+?/.+?/)")

    # grab package names from Alpine distro
    # - also list currently-scraped packages
    with contextlib.closing(sqlite3.connect("alpine.db")) as conn:
        distro_packages = conn.execute(query_packages).fetchall()

        cursor = conn.execute("select distinct(package) from package_tags")
        prev_packages = set((row[0] for row in cursor.fetchall()))

    # per package, scrape the list of tags
    package_tags = {}
    for package, source in distro_packages[:10]:
        if package in prev_packages:
            print(f"package={package}: done, skipping")
            continue
        try:
            repos = repos_pat.search(source).group(1)
        except AttributeError:
            print(f"package={package}: source={source}, repos not found")
            continue
        tags = list_tags(repos)
        print(f"{package}: {len(tags)}")
        if not tags:
            # TODO: handle this case; store in db
            print(f"package={package}: tags not found")
            continue
        package_tags[package] = tags

    # save the tags to a database
    with contextlib.closing(sqlite3.connect("alpine.db")) as conn:
        conn.execute(
            """
            create table if not exists package_tags (
            package TEXT, tag TEXT
            )"""
        )
        conn.commit()
        sql_insert = "insert into package_tags values (?, ?)"
        for package, tags in package_tags.items():
            for tag in tags:
                conn.execute(sql_insert, (package, tag))
            conn.commit()

    # validate package-tags count
    print("SUMMARY")
    with contextlib.closing(sqlite3.connect("alpine.db")) as conn:
        package_tags_count = query1(conn, count="package_tags")
        package_count = query1(conn, sql="""
            select count(distinct(package)) from package_tags
            """)

        distro_count = query1(conn, count="alpine")
        d_github_count = query1(conn, sql="""
            select count(*) from alpine where
            source like '%github.com/%'
            """)

        print("alpine distro:")
        print(f" - {distro_count} packages")
        print(f" - {d_github_count} in GitHub")
        print("package_tags:")
        print(f" - {package_tags_count} rows")
        print(f" - {package_count} packages")


if __name__ == "__main__":
    main()
