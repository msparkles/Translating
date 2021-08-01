import os
import re
import shutil
from pathlib import Path
from typing import List

pattern = re.compile("\\d+-.*")

src = Path('src')


def find_artist_and_album(file: Path, result: List[str] = None):
    """Finds the artist and the album in the path"""
    if result is None:
        result = []

    parent = file.parent
    parent_name = parent.name

    if not parent.exists():
        return result
    if parent_name == "src":
        return result

    if not (parent_name.startswith('-')):
        result.append(
            parent_name.replace(' ', '_')
        )

    return find_artist_and_album(parent, result)


def make_dir(path: Path):
    if path.exists():
        return

    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def export(dirs: List[str], path: Path) -> Path:
    """Creates the directories

    :param dirs: The directories
    :param path: The initial path
    :returns: The final path. e.g. path/dir0/dir1/dir2 of dirs of ["dir0", "dir1", "dir2"]
    """
    if len(dirs) == 0:
        return path

    __dir = dirs.pop(0)

    path = path.joinpath(__dir)

    make_dir(path)

    return export(dirs, path)


def read_files() -> List[Path]:
    """Read the files and store them into a list.

    This is needed due to concurrent issues.

    Searching for the files while writing to the destination would cause a second copy to appear.

    This is fixed via caching the searched files first."""
    paths = []

    for path in src.rglob('*.md'):
        paths.append(path)
    for path in src.rglob('*.url'):
        paths.append(path)
    for path in src.rglob('*.desktop'):
        paths.append(path)

    return paths


def init() -> Path:
    """Initializes the environment.

    It removes the dir and then create a new one."""
    export_path = Path('docs')

    shutil.rmtree(export_path, ignore_errors=True)

    export_path.mkdir()

    return export_path


def rename(old_path: Path, new_name: str) -> Path:
    """renames the file
    """
    new_name = new_name.replace(' ', '_')

    return old_path.parent.joinpath(new_name)


def main():
    """Main part of the script.

    This script is used to export the markdown files to the format used in the cdn repo."""
    export_path = init()

    for path in read_files():
        name = path.name

        if path.stem.casefold() in ['readme', 'index']:
            continue

        parents = find_artist_and_album(path)
        parents.reverse()

        destination = export(parents, export_path)
        copied = shutil.copy2(path, destination)
        os.rename(copied, rename(Path(copied), name))


main()
