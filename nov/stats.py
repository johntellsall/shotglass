#!/usr/bin/env python3

import logging
import subprocess
import sys
import time
from pathlib import Path

cmd_index = "python3 ./build.py index".split()

logging.basicConfig(
    format="%(asctime)s %(message)s", level=logging.INFO, stream=sys.stdout
)

for path_str in sys.argv[1:]:
    path = Path(path_str)
    if path.is_file():
        continue
    logging.info(path.name)
    start = time.time()
    proc = subprocess.run(
        cmd_index + [path], capture_output=True, text=True, check=False
    )
    print(proc.stdout)
    elapsed = time.time() - start
    logging.info("%s done: %.1f seconds", path.name, elapsed)
