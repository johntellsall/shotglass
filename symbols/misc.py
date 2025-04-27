
import concurrent.futures as conc

# XX: always takes ~ 30 seconds for calling `ctags` on 24 files
# - sequential version is only 14 seconds
# 
def query_project_symbols(project_path):
    max_workers = 1
    pool_exec = conc.ThreadPoolExecutor(max_workers=max_workers)

    project_path = Path(project_path)
    src_paths = list(project_path.rglob("*.py")) # FIXME:

    symbols = {}
    with pool_exec as executor:
        # Submit all tasks at once
        future_dict = {executor.submit(run.run_ctags, src_path): src_path
                    for src_path in src_paths}
        for future in conc.as_completed(future_dict):
            src_path = future_dict[future]
            symbols[src_path] = list(future.result())

    # translate back into project-relative paths
    for fullpath in list(symbols.keys()):
        relpath = fullpath.relative_to(project_path)
        symbols[relpath] = symbols.pop(fullpath)
    return symbols



# TODO: how do we assoc release with symbol? Needed?
def db_add_symbols_from_hash(con, project_path, filehash, path):
    """
    Given a hash, extract file, parse symbols from file, add to database
    """
    if not path.endswith(".py"):  # TODO:
        click.echo(f"{path=}: unsupported language")
        return

    # don't warn if __init__ or __manifest__ files are empty
    # - symbols always added, this just suppresses warning
    def is_dull(path):
        return path.endswith("__.py")

    sql = "select id from file where hash=?"
    file_id = query1(con, sql=sql, args=[filehash])

    # copy file from Git to filesystem (uncompress if needed)
    # FIXME: support other languages
    run.run_blob(f"git -C {project_path} show {filehash} > .temp.py")

    # parse symbols from source file
    items = list(run.run_ctags(".temp.py"))
    if not items:
        if not is_dull(path):
            click.secho(f"- {path=}: no symbols")
        return

    # insert symbols into database
    insert_sym = f"""
    insert into symbol (
        name, path, line_start, line_end, kind, file_id
    ) values (
        :name, '{path}', :line, :end, :kind, {file_id})
    """
    con.executemany(insert_sym, IterFixedFields(items))


# class IterFixedFields:
#     """
#     translate between Ctags verbose output and our modest table.
#     Ensure dict-like items have all required fields
#     - ex: "end" is not always provided by Ctags
#     """

#     FIELDS = ("name", "path", "start", "end", "kind")

#     def __init__(self, items):
#         self.items = items
#         self.proto = dict.fromkeys(self.FIELDS)

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if not self.items:
#             raise StopIteration
#         item = self.proto.copy()
#         item.update(self.items.pop(0))
#         return item


# TODO: how do we assoc release with symbol? Needed?
def db_add_symbols_from_hash(con, project_path, filehash, path):
    """
    Given a hash, extract file, parse symbols from file, add to database
    """
    if not path.endswith(".py"):  # TODO:
        click.echo(f"{path=}: unsupported language")
        return

    # don't warn if __init__ or __manifest__ files are empty
    # - symbols always added, this just suppresses warning
    def is_dull(path):
        return path.endswith("__.py")

    sql = "select id from file where hash=?"
    file_id = query1(con, sql=sql, args=[filehash])

    # copy file from Git to filesystem (uncompress if needed)
    # FIXME: support other languages
    run.run_blob(f"git -C {project_path} show {filehash} > .temp.py")

    # parse symbols from source file
    items = list(run.run_ctags(".temp.py"))
    if not items:
        if not is_dull(path):
            click.secho(f"- {path=}: no symbols")
        return

    # insert symbols into database
    insert_sym = f"""
    insert into symbol (
        name, path, line_start, line_end, kind, file_id
    ) values (
        :name, '{path}', :line, :end, :kind, {file_id})
    """
    con.executemany(insert_sym, IterFixedFields(items))


def db_add_symbols_from_path(con, project_path, relpath):
    """
    Given a single file path, parse symbols from file, add to database
    """
    if not relpath.endswith(".py"):  # TODO:
        click.echo(f"{relpath=}: unsupported language")
        return

    # don't warn if __init__ or __manifest__ files are empty
    # - symbols always added, this just suppresses warning
    def is_dull(path):
        return path.endswith("__.py")

    srcpath = Path(project_path) / relpath
    # parse symbols from source file
    items = list(run.run_ctags(srcpath))
    if not items:
        if not is_dull(relpath):
            click.secho(f"- {relpath=}: no symbols")
        return

    # insert symbols into database
    # FIXME: use db_insert_symbols
    insert_sym = f"""
    insert into symbol (
        name, path, line_start, line_end, kind
    ) values (
        :name, '{relpath}', :line, :end, :kind
    )
    """
    con.executemany(insert_sym, IterFixedFields(items))


# TODO: add via *hash* not path
def db_add_files(con, path, project_id, release, only_interesting):
    """
    for project and release/tag, add interesting files into db
    """
    all_items = list(run.git_ls_tree(path, release=release))
    items = list(
        goodsource.filter_good_paths(all_items, only_interesting=only_interesting)
    )
    if not items:
        click.secho(f"{path}: {release=}: no files")
        return

    insert_file = (
        "insert into file (project_id, release, path, hash, size_bytes)"
        f" values ({project_id}, '{release}', :path, :hash, :size_bytes)"
    )
    con.executemany(insert_file, items)


  
def OLD_do_add_symbols(con, project_path):
    """
    list files from database (one project only)
    - parse each file for symbols
    - add symbols to database
    """

    # Per file: extract symbols
    # TODO: restrict to interesting releases+files?
    project_id = db_get_project_id(con, project_path)
    project_name = Path(project_path).name

    sql = f"select count(distinct release) from file where project_id={project_id}"
    assert query1(con, sql=sql) == 1, "FIXME: handle multiple releases"

    click.secho(f"{project_name}: adding symbols", fg="cyan")
    sql = f"select path, hash, release from file where project_id={project_id}"
    batch = 5

    for num, (path, filehash, _release) in enumerate(con.execute(sql)):
        if not num or (num + 1) % batch == 0:
            click.secho(f"- {num+1:03d} {path=} {filehash=}")
            batch = min(batch * 2, 50)

        # TODO: more work here
        if 0:
            db_add_symbols(con, project_path, filehash=filehash, path=path)
        else:
            db_add_symbols_from_path(con, project_path, relpath=path)
    con.commit()
