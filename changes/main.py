import click

@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(files):
    """Print contents of each file passed as argument."""
    for file_path in files:
        with open(file_path, 'r') as f:
            print(f'--- {file_path} ---')
            print(f.read())

if __name__ == '__main__':
    main()