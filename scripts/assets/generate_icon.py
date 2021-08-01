import os
from pathlib import Path

import yaml


def main():
    path = Path('__icons')
    data = {}

    for file in path.glob('*'):
        name = file.name
        extension = os.path.splitext(name)[0]
        data[name] = {'extensions': extension}

    with open('generated_icons.yml', 'w') as stream:
        yaml.dump(data, stream, )


if __name__ == '__main__':
    main()
