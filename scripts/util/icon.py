import logging
from pathlib import Path
from shutil import copyfile
from typing import List, Optional

import yaml

from .assets import Assets

icon_folder = Path().joinpath('.icons')


class Icon:
    def __init__(self, source: Path, name: str, extensions: List[str]):
        self.source = source
        self.name = name
        self.extensions = extensions

    def __str__(self):
        return f"Icon(source={self.source}, name={self.name}, extensions={self.extensions})"

    @property
    def relative_path(self):
        return icon_folder.joinpath(self.name)

    def copy_to(self, destination: Path):
        if not destination.exists():
            logging.info(f"Copying Icon {destination}")
            copyfile(self.source, destination)


class IconManager:
    icons = []

    def read_icons(self, assets: Assets):
        with open(assets.icon_setting(), 'r') as stream:
            try:
                file = yaml.safe_load(stream)
                names = file.keys()

                for name in names:
                    extensions = file.get(name).get('extensions').split(',')
                    source = assets.icon_folder().joinpath(name)

                    icon = Icon(source, name, extensions)
                    logging.info(f"Read {icon}")

                    self.icons.append(icon)
            except yaml.YAMLError as e:
                print(e)

    def lookup(self, extension: str) -> Optional[Icon]:
        for icon in self.icons:
            if extension in icon.extensions:
                return icon
        return self.lookup('__unknown')

    @property
    def go_up_icon(self):
        return self.lookup('__go-up')
