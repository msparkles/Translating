import time
from pathlib import Path

from . import byte_translate, icon_manager, url
from .icon import Icon
from .template import Template


def add_hidden_prefix(name: str) -> str:
    if name.startswith('__'):
        return name
    return '.' + name


class File:
    def __url(self, path: Path):
        self.filename = path.stem
        self.is_url_file = True
        self.url = path.parent.joinpath(add_hidden_prefix(path.stem))

        self.__url = url.get_url_from_path(path)

    def __init__(self, path: Path):
        self.root = path.parent
        self.is_dir = path.is_dir()

        if path.suffix == '.desktop' and url.is_desktop_link(path):
            self.__url(path)
        elif path.suffix == '.url':
            self.__url(path)
        else:
            self.filename = path.name
            self.is_url_file = False
            self.url = path

    def __str__(self):
        return self.url.__str__()

    @property
    def hidden(self) -> bool:
        return self.filename.startswith('__')

    @property
    def extension(self) -> str:
        if self.is_dir:
            return '__folder'
        return self.url.suffix[1:]

    @property
    def icon(self) -> Icon:
        return icon_manager.lookup(self.extension)

    @property
    def size(self) -> str:
        if self.is_url_file:
            size = 0
        elif self.is_dir:
            size = sum(f.stat().st_size for f in self.url.rglob('*') if f.is_file())
        else:
            size = self.url.stat().st_size

        return byte_translate.translate(size)

    @property
    def modified(self):
        if self.is_url_file:
            return '-'

        return time.ctime(self.url.stat().st_mtime)

    def make_url_file(self, template: Template):
        if not self.is_url_file:
            return
        html = template.url_template.replace('{URL}', self.__url)
        if not self.url.exists():
            self.url.mkdir()
        self.url.joinpath('index.html').write_text(html)

    def to_html(self, template: Template) -> str:
        if self.is_url_file:
            self.make_url_file(template)
        return template.file_template.replace('#FILENAME', self.filename) \
            .replace('#URL', self.url.relative_to(self.root).__str__()) \
            .replace('#ICON', self.icon.relative_path.as_posix()) \
            .replace('#SIZE', self.size) \
            .replace('#MODIFIED', self.modified)
