import re
from pathlib import Path

__url_pattern = re.compile('URL=(.*)')
__desktop_type_pattern = re.compile('Type=(.*)')

def get_url_from_path(path: Path) -> str:
    return __url_pattern.search(path.read_text()).group(1)

def is_desktop_link(path: Path) -> bool:
    return __desktop_type_pattern.search(path.read_text()).group(1) == 'Link'