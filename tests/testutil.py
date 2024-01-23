import os
from pathlib import Path

import yaml


def create_dirs_and_files_from_yaml(base_dir, yaml_input):
    # Load the yaml
    dir_structure = yaml.safe_load(yaml_input)

    # Recursive function to create directories/files
    def create(item, path):
        if isinstance(item, dict):
            for k, v in item.items():
                new_path = Path(path) / k
                create(v, new_path)
        elif isinstance(item, str):
            os.path.exists(Path(path)) or os.makedirs(Path(path))
            open(Path(path) / item, 'w').close()
        elif isinstance(item, list):
            for i in item:
                create(i, path)

    create(dir_structure, base_dir.name)

    return base_dir
