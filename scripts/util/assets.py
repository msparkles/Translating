from pathlib import Path


class Assets:
    def __init__(self, path: Path):
        self.path = path

    def icon_folder(self):
        return self.path.joinpath('__icons')

    def icon_setting(self):
        return self.path.joinpath('icons.yml')

    def index_template(self):
        return self.path.joinpath('__index_template.html')

    def file_template(self):
        return self.path.joinpath('__file_template.html')

    def url_template(self):
        return self.path.joinpath('__url_template.html')
