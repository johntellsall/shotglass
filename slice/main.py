import run

def main():
    paths = run.git_ls_files('../SOURCE/hello', 'HEAD', '**/*.c')
    assert 0, paths


if __name__ == "__main__":
    main()
