from .assets import Assets


class Template:
    def __init__(self, assets: Assets, title, parent_dir, filename, size, modified):
        self.index_template = assets.index_template() \
            .read_text() \
            .replace("{TITLE}", title) \
            .replace("{PARENT}", parent_dir) \
            .replace("{FILENAME}", filename) \
            .replace("{SIZE}", size) \
            .replace("{MODIFIED}", modified)
        self.file_template = assets.file_template().read_text()
        self.url_template = assets.url_template().read_text()