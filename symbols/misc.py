
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
