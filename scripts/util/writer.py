import logging
from typing import List

from .index import Index
from .template import Template


def write(template: Template, indexes: List[Index]):
    for index in indexes:
        path = index.path.joinpath('index.html')
        logging.info(f"Writing {path}")

        html = index.to_html(template)

        path.write_text(html)


def write_deep(template: Template, indexes: List[Index]):
    if len(indexes) <= 0:
        return

    write(template, indexes)

    for index in indexes:
        write_deep(template, index.list_sub_indexes())
