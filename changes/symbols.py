# symbols.py
# - list symbols (names, line numbers) in source code file
# - render based on length

from dataclasses import dataclass
import run
import math

@dataclass
class Symbol:
    name: str
    line: int
    length: int

@dataclass
class SymbolFile:
    path: str
    num_lines: int
    symbols: list[Symbol]


def count_lines(path: str) -> int:
    """Count the number of lines in a file."""
    with open(path, 'r', encoding='utf-8') as file:
        return sum(1 for _ in file)


def parse_path(path: str) -> SymbolFile:
    """
    Parse a source code file to extract symbols and their line numbers.
    """
    symbols = list(run.run_ctags(paths=[path]))
    symfile = SymbolFile(
        path=path,
        num_lines=count_lines(path),
        symbols=symbols)
    return symfile


def render(symfile: SymbolFile):
    size = math.ceil(math.sqrt(symfile.num_lines))
