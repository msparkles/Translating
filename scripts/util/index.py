import os
from pathlib import Path
from typing import List

from . import reader, icon_manager
from .file import File
from .icon import icon_folder, Icon
from .reader import check_invalid
from .template import Template


class Index:
    def __init__(self, path: Path, files: List[File]):
        self.path = path
        self.files = files
        self.icon_folder = path.joinpath(icon_folder)

    @classmethod
    def read_from_path(cls, path: Path):
        return cls(path, reader.list_files(path))

    def list_sub_indexes(self):
        sub_indexes = []

        for directory in self.path.iterdir():
            if directory.is_dir():
                if directory.name.startswith('.'):
                    continue
                sub_indexes.append(Index.read_from_path(directory))
        return sub_indexes

    def icon(self, icon: Icon):
        icon_path = self.icon_folder.joinpath(icon.name)

        if (not icon_path.exists()):
            icon.copy_to(icon_path)

    def files_to_html(self, template: Template) -> str:
        strings = []

        # create the icon folder
        if not self.icon_folder.exists():
            os.makedirs(self.icon_folder)

        # copy the go up icon
        self.icon(icon_manager.go_up_icon)

        # sort by name
        self.files.sort(key=lambda f: f.filename)
        # sort folders to top
        self.files.sort(key=lambda f: not f.is_dir)

        for file in self.files:
            # to_html is still called for side effects
            html = file.to_html(template)

            if not file.hidden:
                strings.append(html)
                self.icon(file.icon)

        return ''.join(strings)

    def to_html(self, template: Template) -> str:
        return template.index_template.replace('#DIR', self.path.as_posix()) \
            .replace('#TITLE', self.path.name) \
            .replace('#FILES', self.files_to_html(template))
