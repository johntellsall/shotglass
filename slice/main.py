from pathlib import Path
import sys
import run


def proj_list_paths(projtop):
    base = Path(projtop)
    rel_paths = run.git_ls_files(projtop, 'HEAD', '**/*.c')

    paths = [base / relpath for relpath in rel_paths]
    return paths


def main(proj_list):
    for projtop in proj_list:
        name = Path(projtop).stem
        paths = proj_list_paths(projtop)
        print(f'{name}: {len(paths)} source files')

        symbols = list(run.run_ctags(paths))
        print(f'{name}: {len(symbols)} symbols')


if __name__ == "__main__":
    main(sys.argv[1:])
