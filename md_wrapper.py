import os
from pathlib import Path
from shutil import move
import shutil
import markdown

__template = Path('md_wrapper_template.html').read_text()


def to_html(path: Path, md):
    return __template.replace('{NAME}', path.name)\
                     .replace('{MD}', md)


def read_files(path: Path):
    return filter(lambda f: not f.is_dir(), list(path.rglob('*.md')))


def main():
    for file in read_files(Path('docs')):
        directory = file
        html = directory.joinpath('index.html')

        filedata = file.read_text()

        md = markdown.markdown(filedata, extensions=['markdown.extensions.tables'])

        file = file.rename(directory.parent.joinpath("./__temp__"))

        directory.mkdir()
        html.write_text(to_html(html, md))

        shutil.copystat(file, html)

        file.unlink()


main()
