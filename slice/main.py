from pathlib import Path
import run

def main():
    rel_paths = run.git_ls_files('../SOURCE/hello', 'HEAD', '**/*.c')
    print(f'hello: {len(rel_paths)} source files')

    base = Path('../SOURCE/hello')
    paths = [base / relpath for relpath in rel_paths]
    symbols = list(run.run_ctags(paths, verbose=True))
    print(f'hello: {len(symbols)} symbols')


if __name__ == "__main__":
    main()
