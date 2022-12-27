"""
Creates the AoC folder structure.

Usage: python mk-folder.py [day] [year]
"""

from datetime import date
from pathlib import Path
import sys
import os
import shutil

match sys.argv:
    case [_]:
        d = date.today()
    case [_, day]:
        d = date(date.today().year, 12, int(day))
    case [_, day, year]:
        d = date(int(year), 12, int(day))
    case _:
        raise ValueError(f"Command line args {sys.argv[1:]} not allowed")

os.chdir(Path(__file__).absolute().parent)

day_str = f"day{d.day:02d}"
path = Path(str(d.year)) / day_str

if path.exists():
    ans = input(f"Path {path} exists! Continue anyway? [yN]")
    if ans.lower() != "y" and ans.lower() != "yes":
        sys.exit(0)
    else:
        shutil.rmtree(path)

path.mkdir(parents=True)
for file in [f"{day_str}-1.py", f"{day_str}-2.py", "example.txt", "input.txt"]:
    (path / file).touch()
